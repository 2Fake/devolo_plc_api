import asyncio
import ipaddress
import logging
import struct
from datetime import date
from typing import Dict, Optional

import httpx
from zeroconf import ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf

from .device_api.deviceapi import DeviceApi
from .exceptions.device import DeviceNotFound
from .plcnet_api.plcnetapi import PlcNetApi

EMPTY_INFO: Dict = {
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
                 plcnetapi: Optional[Dict] = None,
                 deviceapi: Optional[Dict] = None,
                 zeroconf_instance: Optional[Zeroconf] = None):
        self.firmware_date = date.fromtimestamp(0)
        self.firmware_version = ""
        self.hostname = ""
        self.ip = ip
        self.mac = ""
        self.mt_number = 0
        self.product = ""
        self.technology = ""
        self.serial_number = 0

        self.device = None
        self.plcnet = None

        self._connected = False
        self._info: Dict = {
            "_dvl-plcnetapi._tcp.local.": plcnetapi or EMPTY_INFO,
            "_dvl-deviceapi._tcp.local.": deviceapi or EMPTY_INFO,
        }
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._password = ""
        self._session_instance: Optional[httpx.AsyncClient] = None
        self._zeroconf_instance = zeroconf_instance
        logging.captureWarnings(True)

        self._loop: asyncio.AbstractEventLoop
        self._session: httpx.AsyncClient
        self._zeroconf: Zeroconf

    def __del__(self):
        if self._connected and self._session_instance is None:
            self._logger.warning("Please disconnect properly from the device.")

    async def __aenter__(self):
        await self.async_connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.async_disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def password(self) -> str:
        """ The currently set device password. """
        return self._password

    @password.setter
    def password(self, password: str):
        """ Change the currently set device password. """
        self._password = password
        if self.device:
            self.device.password = password

    async def async_connect(self, session_instance: Optional[httpx.AsyncClient] = None):
        """
        Connect to a device asynchronous.

        :param: session_instance: Session client instance to be potentially reused.
        """
        self._loop = asyncio.get_running_loop()
        self._session_instance = session_instance
        self._session = self._session_instance or httpx.AsyncClient()
        self._zeroconf = self._zeroconf_instance or Zeroconf()
        await asyncio.gather(self._get_device_info(), self._get_plcnet_info())
        if not self.device and not self.plcnet:
            raise DeviceNotFound(f"The device {self.ip} did not answer.")
        self._connected = True

    def connect(self):
        """ Connect to a device synchronous. """
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self.async_connect())

    async def async_disconnect(self):
        """ Disconnect from a device asynchronous. """
        if not self._zeroconf_instance:
            self._zeroconf.close()
        if not self._session_instance:
            await self._session.aclose()
        self._connected = False

    def disconnect(self):
        """ Disconnect from a device asynchronous. """
        self._loop.run_until_complete(self.async_disconnect())
        self._loop.close()

    async def _get_device_info(self):
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

    async def _get_plcnet_info(self):
        """ Get information from the devolo PlcNet API. """
        service_type = "_dvl-plcnetapi._tcp.local."
        try:
            await asyncio.wait_for(self._get_zeroconf_info(service_type=service_type), timeout=3)
        except asyncio.TimeoutError:
            return

        self.mac = self._info[service_type]["properties"]["PlcMacAddress"]
        self.technology = self._info[service_type]["properties"].get("PlcTechnology", "")

        self.plcnet = PlcNetApi(ip=self.ip, session=self._session, info=self._info[service_type])

    async def _get_zeroconf_info(self, service_type: str):
        """ Browse for the desired mDNS service types and query them. """
        if self._info[service_type]["properties"]:
            return  # No need to continue, if device info already exist

        self._logger.debug("Browsing for %s", service_type)
        browser = ServiceBrowser(self._zeroconf, service_type, [self._state_change], addr=self.ip)
        while not self._info[service_type]["properties"]:
            await asyncio.sleep(0.1)
        browser.cancel()

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """ Evaluate the query result. """
        service_info = zeroconf.get_service_info(service_type, name)

        if service_info is None or str(ipaddress.ip_address(service_info.addresses[0])) != self.ip:
            return  # No need to continue, if there are no relevant service information

        if state_change is ServiceStateChange.Added:
            self._logger.debug("Adding service info of %s", service_type)
            self._info[service_type] = self.info_from_service(service_info)

    @staticmethod
    def info_from_service(service_info: ServiceInfo) -> Optional[Dict]:
        """ Return prepared info from mDNS entries. """
        properties = {}
        if not service_info.addresses:
            return None  # No need to continue, if there is no IP address to contact the device

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
