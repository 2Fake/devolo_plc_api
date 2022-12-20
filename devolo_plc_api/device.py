"""Representation of your devolo device."""
from __future__ import annotations

import asyncio
import ipaddress
import logging
import struct
from contextlib import suppress
from datetime import date
from types import TracebackType
from typing import Any

import httpx
from zeroconf import DNSQuestionType, ServiceInfo, ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from .device_api import SERVICE_TYPE as DEVICEAPI
from .device_api import DeviceApi
from .exceptions.device import DeviceNotFound
from .plcnet_api import DEVICES_WITHOUT_PLCNET
from .plcnet_api import SERVICE_TYPE as PLCNETAPI
from .plcnet_api import PlcNetApi

EMPTY_INFO: dict[str, Any] = {"properties": {}}


class Device:  # pylint: disable=too-many-instance-attributes
    """
    Representing object for your devolo PLC device. It stores all properties and functionalities discovered during setup.

    :param ip: IP address of the device to communicate with.
    :param plcnetapi: Reuse externally gathered data for the plcnet API
    :param deviceapi: Reuse externally gathered data for the device API
    :param zeroconf_instance: Zeroconf instance to be potentially reused.
    """

    def __init__(
        self,
        ip: str,
        plcnetapi: dict[str, Any] | None = None,
        deviceapi: dict[str, Any] | None = None,
        zeroconf_instance: AsyncZeroconf | Zeroconf | None = None,
    ) -> None:
        self.ip = ip
        self.mac = ""
        self.mt_number = 0
        self.product = ""
        self.technology = ""
        self.serial_number = 0

        self.device: DeviceApi | None = None
        self.plcnet: PlcNetApi | None = None

        self._browser: dict[str, AsyncServiceBrowser] = {}
        self._connected = False
        self._info: dict[str, dict[str, Any]] = {
            PLCNETAPI: plcnetapi or EMPTY_INFO,
            DEVICEAPI: deviceapi or EMPTY_INFO,
        }
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._multicast = False
        self._password = ""
        self._session_instance: httpx.AsyncClient | None = None
        self._zeroconf_instance = zeroconf_instance
        logging.captureWarnings(True)

        self._session: httpx.AsyncClient
        self._zeroconf: AsyncZeroconf

    def __del__(self) -> None:
        if self._connected and self._session_instance is None:
            self._logger.warning("Please disconnect properly from the device.")

    async def __aenter__(self) -> Device:
        await self.async_connect()
        return self

    async def __aexit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        await self.async_disconnect()

    def __enter__(self) -> Device:
        self.connect()
        return self

    def __exit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        self.disconnect()

    @property
    def firmware_date(self) -> date:
        """Date the firmware was built."""
        if DEVICEAPI in self._info:
            return date.fromisoformat(self._info[DEVICEAPI]["properties"].get("FirmwareDate", "1970-01-01")[:10])
        return date.fromtimestamp(0)

    @property
    def firmware_version(self) -> str:
        if DEVICEAPI in self._info:
            return self._info[DEVICEAPI]["properties"].get("FirmwareVersion", "")
        return ""

    @property
    def hostname(self) -> str:
        if DEVICEAPI in self._info:
            return self._info[DEVICEAPI].get("hostname", "")
        return ""

    @property
    def password(self) -> str:
        """The currently set device password."""
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        """Change the currently set device password."""
        self._password = password
        if self.device:
            self.device.password = password

    async def async_connect(self, session_instance: httpx.AsyncClient | None = None) -> None:
        """
        Connect to a device asynchronous.

        :param: session_instance: Session client instance to be potentially reused.
        """
        self._session_instance = session_instance
        self._session = self._session_instance or httpx.AsyncClient()
        if not self._zeroconf_instance:
            self._zeroconf = AsyncZeroconf()
        elif isinstance(self._zeroconf_instance, Zeroconf):
            self._zeroconf = AsyncZeroconf(zc=self._zeroconf_instance)
        else:
            self._zeroconf = self._zeroconf_instance
        await asyncio.gather(self._get_device_info(), self._get_plcnet_info())
        if not self.device and not self.plcnet:
            raise DeviceNotFound(f"The device {self.ip} did not answer.")
        self._connected = True

    def connect(self) -> None:
        """Connect to a device synchronous."""
        asyncio.run(self.async_connect())

    async def async_disconnect(self) -> None:
        """Disconnect from a device asynchronous."""
        if self._connected:
            for browser in self._browser.values():
                await browser.async_cancel()
            if not self._zeroconf_instance:
                await self._zeroconf.async_close()
            if not self._session_instance:
                await self._session.aclose()
            self._connected = False

    def disconnect(self) -> None:
        """Disconnect from a device synchronous."""
        asyncio.run(self.async_disconnect())

    async def _get_device_info(self) -> None:
        """Get information from the devolo Device API."""
        service_type = DEVICEAPI
        await self._get_zeroconf_info(service_type=service_type)
        if not self._info[service_type]["properties"]:
            await self._retry_zeroconf_info(service_type=service_type)
        if self._info[service_type]["properties"]:
            self.mt_number = self._info[service_type]["properties"].get("MT", 0)
            self.product = self._info[service_type]["properties"].get("Product", "")
            self.serial_number = self._info[service_type]["properties"]["SN"]
            self.device = DeviceApi(ip=self.ip, session=self._session, info=self._info[service_type])
            self.device.password = self.password

    async def _get_plcnet_info(self) -> None:
        """Get information from the devolo PlcNet API."""
        service_type = PLCNETAPI
        if self.mt_number in DEVICES_WITHOUT_PLCNET:
            return
        await self._get_zeroconf_info(service_type=service_type)
        if not self._info[service_type]["properties"] and self.mt_number not in DEVICES_WITHOUT_PLCNET:
            await self._retry_zeroconf_info(service_type=service_type)
        if self._info[service_type]["properties"]:
            self.mac = self._info[service_type]["properties"]["PlcMacAddress"]
            self.technology = self._info[service_type]["properties"].get("PlcTechnology", "")
            self.plcnet = PlcNetApi(ip=self.ip, session=self._session, info=self._info[service_type])

    async def _get_zeroconf_info(self, service_type: str) -> None:
        """Browse for the desired mDNS service types and query them."""
        self._logger.debug("Browsing for %s", service_type)
        counter = 0
        addr = None if self._multicast else self.ip
        question_type = DNSQuestionType.QM if self._multicast else DNSQuestionType.QU
        self._browser[service_type] = AsyncServiceBrowser(
            zeroconf=self._zeroconf.zeroconf,
            type_=service_type,
            handlers=[self._state_change],
            addr=addr,
            question_type=question_type,
        )
        while not self._info[service_type]["properties"] and counter < 300:
            counter += 1
            await asyncio.sleep(0.01)

    async def _retry_zeroconf_info(self, service_type: str) -> None:
        """Retry getting the zeroconf info using multicast."""
        self._logger.debug(
            "Having trouble getting %s via unicast messages. Switching to multicast for this device.", service_type
        )
        self._multicast = True
        await self._get_zeroconf_info(service_type=service_type)

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        """Evaluate the query result."""
        if state_change == ServiceStateChange.Removed:
            return
        asyncio.create_task(self._get_service_info(zeroconf, service_type, name))

    async def _get_service_info(self, zeroconf: Zeroconf, service_type: str, name: str) -> None:
        """Get service information, if IP matches."""
        service_info = AsyncServiceInfo(service_type, name)
        question_type = DNSQuestionType.QM if self._multicast else DNSQuestionType.QU
        with suppress(RuntimeError):
            await service_info.async_request(zeroconf, timeout=1000, question_type=question_type)

        if (
            service_info is None
            or not service_info.addresses
            or str(ipaddress.ip_address(service_info.addresses[0])) != self.ip
        ):
            return  # No need to continue, if there are no relevant service information

        self._logger.debug("Updating service info of %s for %s", service_type, service_info.server_key)
        self._info[service_type] = self.info_from_service(service_info)

    @staticmethod
    def info_from_service(service_info: ServiceInfo) -> dict[str, Any]:
        """Return prepared info from mDNS entries."""
        properties = {}
        if not service_info.addresses:
            return {}  # No need to continue, if there is no IP address to contact the device

        total_length = len(service_info.text)
        offset = 0
        while offset < total_length:
            (parsed_length,) = struct.unpack_from("!B", service_info.text, offset)
            key_value = service_info.text[offset + 1 : offset + 1 + parsed_length].decode("UTF-8").split("=")
            properties[key_value[0]] = key_value[1]
            offset += parsed_length + 1

        address = service_info.addresses[0]

        return {
            "address": str(ipaddress.ip_address(address)),
            "hostname": service_info.server,
            "port": service_info.port,
            "properties": properties,
        }
