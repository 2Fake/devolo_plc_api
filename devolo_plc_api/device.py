from __future__ import annotations

import asyncio
import ipaddress
import logging
import struct
from datetime import date
from types import TracebackType
from typing import Any

import httpx
from zeroconf import DNSQuestionType, ServiceInfo, ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from .device_api.deviceapi import DeviceApi
from .exceptions.device import DeviceNotFound
from .plcnet_api.plcnetapi import PlcNetApi

EMPTY_INFO: dict[str,
                 Any] = {
                     "properties": {}
                 }


class Device:
    """
    Representing object for your devolo PLC device. It stores all properties and functionalities discovered during setup.

    :param ip: IP address of the device to communicate with.
    :param plcnetapi: Reuse externally gathered data for the plcnet API
    :param deviceapi: Reuse externally gathered data for the device API
    :param zeroconf_instance: Zeroconf instance to be potentially reused.
    """

    def __init__(self,
                 ip: str,
                 plcnetapi: dict[str,
                                 Any] | None = None,
                 deviceapi: dict[str,
                                 Any] | None = None,
                 zeroconf_instance: AsyncZeroconf | None = None) -> None:
        self.firmware_date = date.fromtimestamp(0)
        self.firmware_version = ""
        self.hostname = ""
        self.ip = ip
        self.mac = ""
        self.mt_number = 0
        self.product = ""
        self.technology = ""
        self.serial_number = 0

        self.device: DeviceApi | None = None
        self.plcnet: PlcNetApi | None = None

        self._connected = False
        self._info: dict[str,
                         dict[str,
                              Any]] = {
                                  "_dvl-plcnetapi._tcp.local.": plcnetapi or EMPTY_INFO,
                                  "_dvl-deviceapi._tcp.local.": deviceapi or EMPTY_INFO,
                              }
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._password = ""
        self._session_instance: httpx.AsyncClient | None = None
        self._zeroconf_instance = zeroconf_instance
        logging.captureWarnings(True)

        self._loop: asyncio.AbstractEventLoop
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
    def password(self) -> str:
        """ The currently set device password. """
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        """ Change the currently set device password. """
        self._password = password
        if self.device:
            self.device.password = password

    async def async_connect(self, session_instance: httpx.AsyncClient | None = None) -> None:
        """
        Connect to a device asynchronous.

        :param: session_instance: Session client instance to be potentially reused.
        """
        self._loop = asyncio.get_running_loop()
        self._session_instance = session_instance
        self._session = self._session_instance or httpx.AsyncClient()
        self._zeroconf = self._zeroconf_instance or AsyncZeroconf()
        await asyncio.gather(self._get_device_info(), self._get_plcnet_info())
        if not self.device and not self.plcnet:
            raise DeviceNotFound(f"The device {self.ip} did not answer.")
        self._connected = True

    def connect(self) -> None:
        """ Connect to a device synchronous. """
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self.async_connect())

    async def async_disconnect(self) -> None:
        """ Disconnect from a device asynchronous. """
        if not self._zeroconf_instance:
            await self._zeroconf.async_close()
        if not self._session_instance:
            await self._session.aclose()
        self._connected = False

    def disconnect(self) -> None:
        """ Disconnect from a device asynchronous. """
        self._loop.run_until_complete(self.async_disconnect())
        self._loop.close()

    async def _get_device_info(self) -> None:
        """ Get information from the devolo Device API. """
        service_type = "_dvl-deviceapi._tcp.local."
        try:
            await asyncio.wait_for(self._get_zeroconf_info(service_type=service_type), timeout=3)
        except asyncio.TimeoutError:
            return

        self.firmware_date = date.fromisoformat(self._info[service_type]["properties"].get("FirmwareDate", "1970-01-01"))
        self.firmware_version = self._info[service_type]["properties"].get("FirmwareVersion", "")
        self.hostname = self._info[service_type].get("hostname", "")
        self.mt_number = self._info[service_type]["properties"].get("MT", 0)
        self.product = self._info[service_type]["properties"].get("Product", "")
        self.serial_number = self._info[service_type]["properties"]["SN"]

        self.device = DeviceApi(ip=self.ip, session=self._session, info=self._info[service_type])

    async def _get_plcnet_info(self) -> None:
        """ Get information from the devolo PlcNet API. """
        service_type = "_dvl-plcnetapi._tcp.local."
        try:
            await asyncio.wait_for(self._get_zeroconf_info(service_type=service_type), timeout=3)
        except asyncio.TimeoutError:
            return

        self.mac = self._info[service_type]["properties"]["PlcMacAddress"]
        self.technology = self._info[service_type]["properties"].get("PlcTechnology", "")

        self.plcnet = PlcNetApi(ip=self.ip, session=self._session, info=self._info[service_type])

    async def _get_zeroconf_info(self, service_type: str) -> None:
        """ Browse for the desired mDNS service types and query them. """
        if self._info[service_type]["properties"]:
            return  # No need to continue, if device info already exist

        self._logger.debug("Browsing for %s", service_type)
        browser = AsyncServiceBrowser(self._zeroconf.zeroconf,
                                      service_type,
                                      [self._state_change],
                                      question_type=DNSQuestionType.QM)
        while not self._info[service_type]["properties"]:
            await asyncio.sleep(0.1)
        await browser.async_cancel()

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        """ Evaluate the query result. """
        if state_change is not ServiceStateChange.Added:
            return
        asyncio.ensure_future(self._get_service_info(zeroconf, service_type, name))

    async def _get_service_info(self, zeroconf: Zeroconf, service_type: str, name: str) -> None:
        """ Get service information, if IP matches. """
        service_info = AsyncServiceInfo(service_type, name)
        await service_info.async_request(zeroconf, timeout=3000)

        if service_info is None or str(ipaddress.ip_address(service_info.addresses[0])) != self.ip:
            return  # No need to continue, if there are no relevant service information

        self._logger.debug("Adding service info of %s", service_type)
        self._info[service_type] = self.info_from_service(service_info)

    @staticmethod
    def info_from_service(service_info: ServiceInfo) -> dict[str, Any]:
        """ Return prepared info from mDNS entries. """
        properties = {}
        if not service_info.addresses:
            return {}  # No need to continue, if there is no IP address to contact the device

        total_length = len(service_info.text)
        offset = 0
        while offset < total_length:
            parsed_length, = struct.unpack_from("!B", service_info.text, offset)
            key_value = service_info.text[offset + 1:offset + 1 + parsed_length].decode("UTF-8").split("=")
            properties[key_value[0]] = key_value[1]
            offset += parsed_length + 1

        address = service_info.addresses[0]

        return {
            "address": str(ipaddress.ip_address(address)),
            "hostname": service_info.server,
            "port": service_info.port,
            "properties": properties,
        }
