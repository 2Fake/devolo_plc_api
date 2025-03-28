"""Representation of your devolo device."""

from __future__ import annotations

import asyncio
import logging
from contextlib import suppress
from datetime import date
from ipaddress import ip_address, ip_network
from struct import unpack_from
from typing import TYPE_CHECKING, cast

from httpx import AsyncClient
from ifaddr import get_adapters
from zeroconf import DNSQuestionType, ServiceInfo, ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from .device_api import SERVICE_TYPE as DEVICEAPI, DeviceApi
from .exceptions import DeviceNotFound
from .plcnet_api import DEVICES_WITHOUT_PLCNET, SERVICE_TYPE as PLCNETAPI, PlcNetApi
from .zeroconf import ZeroconfServiceInfo

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self


class Device:
    """
    Representing object for your devolo PLC device. It stores all properties and functionalities discovered during setup.

    :param ip: IP address of the device to communicate with.
    :param plcnetapi: Reuse externally gathered data for the plcnet API
    :param deviceapi: Reuse externally gathered data for the device API
    :param zeroconf_instance: Zeroconf instance to be potentially reused.
    """

    MDNS_TIMEOUT = 300

    def __init__(
        self,
        ip: str,
        zeroconf_instance: AsyncZeroconf | Zeroconf | None = None,
    ) -> None:
        """Initialize the device."""
        self.ip = ip
        self.mac = ""
        self.mt_number = "0"
        self.product = ""
        self.technology = ""
        self.serial_number = "0"

        self.device: DeviceApi | None = None
        self.plcnet: PlcNetApi | None = None

        self._background_tasks: set[asyncio.Task] = set()
        self._browser: AsyncServiceBrowser | None = None
        self._connected = False
        self._info: dict[str, ZeroconfServiceInfo] = {PLCNETAPI: ZeroconfServiceInfo(), DEVICEAPI: ZeroconfServiceInfo()}
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._multicast = False
        self._password = ""
        self._session_instance: AsyncClient | None = None
        self._zeroconf_instance = zeroconf_instance
        logging.captureWarnings(capture=True)

        self._loop: asyncio.AbstractEventLoop
        self._session: AsyncClient
        self._zeroconf: AsyncZeroconf

    def __del__(self) -> None:
        """Warn user, if the connection was not properly closed."""
        if self._connected and self._session_instance is None:
            self._logger.warning("Please disconnect properly from the device.")

    async def __aenter__(self) -> Self:
        """Connect to a device asynchronously when entering a context manager."""
        await self.async_connect()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """Disconnect to a device asynchronously when entering a context manager."""
        await self.async_disconnect()

    def __enter__(self) -> Self:
        """Connect to a device synchronously when leaving a context manager."""
        self.connect()
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """Disconnect to a device synchronously when leaving a context manager."""
        self.disconnect()

    @property
    def firmware_date(self) -> date:
        """Date the firmware was built."""
        return date.fromisoformat(self._info[DEVICEAPI].properties.get("FirmwareDate", "1970-01-01")[:10])

    @property
    def firmware_version(self) -> str:
        """Firmware version currently installed."""
        return self._info[DEVICEAPI].properties.get("FirmwareVersion", "")

    @property
    def hostname(self) -> str:
        """mDNS hostname of the device."""  # noqa: D403
        return self._info[DEVICEAPI].hostname

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
        if self.plcnet:
            self.plcnet.password = password

    async def async_connect(self, session_instance: AsyncClient | None = None) -> None:
        """
        Connect to a device asynchronous.

        :param: session_instance: Session client instance to be potentially reused.
        """
        self._session_instance = session_instance
        self._session = self._session_instance or AsyncClient()
        if not self._zeroconf_instance:
            self._zeroconf = AsyncZeroconf(interfaces=await self._get_relevant_interfaces())
        elif isinstance(self._zeroconf_instance, Zeroconf):
            self._zeroconf = AsyncZeroconf(zc=self._zeroconf_instance)
        else:
            self._zeroconf = self._zeroconf_instance
        await self._get_zeroconf_info()
        if not self._info[DEVICEAPI].properties and not self._info[PLCNETAPI].properties:
            await self._retry_zeroconf_info()
        if not self.device and not self.plcnet:
            raise DeviceNotFound(self.ip)
        self._connected = True

    def connect(self) -> None:
        """Connect to a device synchronous."""
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self.async_connect())

    async def async_disconnect(self) -> None:
        """Disconnect from a device asynchronous."""
        if self._connected:
            if self._browser:
                await self._browser.async_cancel()
            if not self._zeroconf_instance:
                await self._zeroconf.async_close()
            if not self._session_instance:
                await self._session.aclose()
            self._connected = False

    def disconnect(self) -> None:
        """Disconnect from a device synchronous."""
        self._loop.run_until_complete(self.async_disconnect())

    async def _get_relevant_interfaces(self) -> list[str]:
        """Get the IP address of the relevant interface to reduce traffic."""
        interface: list[str] = []
        for adapter in get_adapters():
            interface.extend(
                cast("str", ip.ip)
                for ip in adapter.ips
                if ip.is_IPv4 and ip_address(self.ip) in ip_network(f"{ip.ip}/{ip.network_prefix}", strict=False)
            )
            interface.extend(
                cast("str", ip.ip[0])
                for ip in adapter.ips
                if ip.is_IPv6 and ip_address(self.ip) in ip_network(f"{ip.ip[0]}/{ip.network_prefix}", strict=False)
            )
        return interface

    async def _get_device_info(self) -> None:
        """Get information from the devolo Device API."""
        service_type = DEVICEAPI
        if self._info[service_type].properties:
            self.mt_number = self._info[service_type].properties.get("MT", "0")
            self.product = self._info[service_type].properties.get("Product", "")
            self.serial_number = self._info[service_type].properties["SN"]
            self.device = DeviceApi(
                ip=str(ip_address(self._info[service_type].address)),
                session=self._session,
                info=self._info[service_type],
            )
            self.device.password = self.password

    async def _get_plcnet_info(self) -> None:
        """Get information from the devolo PlcNet API."""
        service_type = PLCNETAPI
        if self._info[service_type].properties:
            self.mac = self._info[service_type].properties["PlcMacAddress"]
            self.technology = self._info[service_type].properties.get("PlcTechnology", "")
            self.plcnet = PlcNetApi(
                ip=str(ip_address(self._info[service_type].address)),
                session=self._session,
                info=self._info[service_type],
            )
            self.plcnet.password = self.password

    async def _get_zeroconf_info(self) -> None:
        """Browse for the desired mDNS service types and query them."""
        service_types = [DEVICEAPI, PLCNETAPI]
        counter = 0
        self._logger.debug("Browsing for %s", service_types)
        addr = None if self._multicast else self.ip
        question_type = DNSQuestionType.QM if self._multicast else DNSQuestionType.QU
        if self._browser:
            await self._browser.async_cancel()
            self._browser = None
        self._browser = AsyncServiceBrowser(
            zeroconf=self._zeroconf.zeroconf,
            type_=service_types,
            handlers=[self._state_change],
            addr=addr,
            question_type=question_type,
        )
        while (
            not self._info[DEVICEAPI].properties
            or (not self._info[PLCNETAPI].properties and self.mt_number not in DEVICES_WITHOUT_PLCNET)
        ) and counter < self.MDNS_TIMEOUT:
            counter += 1
            await asyncio.sleep(0.01)

    async def _retry_zeroconf_info(self) -> None:
        """Retry getting the zeroconf info using multicast."""
        self._logger.debug("Having trouble getting results via unicast messages. Switching to multicast for this device.")
        self._multicast = True
        await self._get_zeroconf_info()

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        """Evaluate the query result."""
        if state_change == ServiceStateChange.Removed:
            return
        task = asyncio.create_task(self._get_service_info(zeroconf, service_type, name))
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.remove)

    async def _get_service_info(self, zeroconf: Zeroconf, service_type: str, name: str) -> None:
        """Get service information, if IP matches."""
        service_info = AsyncServiceInfo(service_type, name)
        update = {
            DEVICEAPI: self._get_device_info,
            PLCNETAPI: self._get_plcnet_info,
        }
        with suppress(RuntimeError):
            if not self._multicast:
                await service_info.async_request(zeroconf, timeout=1000, question_type=DNSQuestionType.QU, addr=self.ip)
            else:
                await service_info.async_request(zeroconf, timeout=1000, question_type=DNSQuestionType.QM)

        if not service_info.addresses or self.ip not in service_info.parsed_addresses():
            return  # No need to continue, if there are no relevant service information

        self._logger.debug("Updating service info of %s for %s", service_type, service_info.server_key)
        if info := self.info_from_service(service_info):
            self._info[service_type] = info
            await update[service_type]()

    @staticmethod
    def info_from_service(service_info: ServiceInfo) -> ZeroconfServiceInfo | None:
        """Return prepared info from mDNS entries."""
        properties = {}
        total_length = len(service_info.text)
        offset = 0
        while offset < total_length:
            (parsed_length,) = unpack_from("!B", service_info.text, offset)
            key_value = service_info.text[offset + 1 : offset + 1 + parsed_length].decode("UTF-8").split("=")
            properties[key_value[0]] = key_value[1]
            offset += parsed_length + 1

        return ZeroconfServiceInfo(
            address=service_info.addresses[0],
            hostname=service_info.server or "",
            port=service_info.port,
            properties=properties,
        )
