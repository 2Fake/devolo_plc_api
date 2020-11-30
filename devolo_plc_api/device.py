import asyncio
import logging
import socket
import struct
from datetime import date
from typing import Dict, Optional

import httpx
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from .device_api.deviceapi import DeviceApi
from .exceptions.device import DeviceNotFound
from .plcnet_api.plcnetapi import PlcNetApi


class Device:
    """
    Representing object for your devolo PLC device. It stores all properties and functionalities discovered during setup.

    :param ip: IP address of the device to communicate with.
    :param zeroconf_instance: Zeroconf instance to be potentially reused.
    """

    def __init__(self, ip: str, zeroconf_instance: Optional[Zeroconf] = None):
        self.firmware_date = date.fromtimestamp(0)
        self.firmware_version = ""
        self.ip = ip
        self.mac = ""
        self.mt_number = 0
        self.product = ""
        self.technology = ""
        self.serial_number = 0

        self.device = None
        self.plcnet = None

        self._info: Dict = {
            "_dvl-plcnetapi._tcp.local.": {},
            "_dvl-deviceapi._tcp.local.": {},
        }
        self._logger = logging.getLogger(self.__class__.__name__)
        self._password = ""
        self._zeroconf_instance = zeroconf_instance

        self._loop: asyncio.AbstractEventLoop
        self._session: httpx.AsyncClient
        self._zeroconf: Zeroconf

    async def __aenter__(self):
        self._loop = asyncio.get_running_loop()
        await self._setup_device()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._zeroconf_instance:
            self._zeroconf.close()
        await self._session.aclose()

    def __enter__(self):
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self._setup_device())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._loop.run_until_complete(self.__aexit__(exc_type, exc_val, exc_tb))
        self._loop.close()

    @property
    def password(self):
        """ The currently set device password. """
        return self._password

    @password.setter
    def password(self, password):
        """ Change the currently set device password. """
        self._password = password
        self.device.password = password

    async def _get_device_info(self):
        """ Get information from the devolo Device API. """
        service_type = "_dvl-deviceapi._tcp.local."
        try:
            await asyncio.wait_for(self._get_zeroconf_info(service_type=service_type), timeout=3)
        except asyncio.TimeoutError:
            return

        self.firmware_date = date.fromisoformat(self._info[service_type].get("FirmwareDate", "1970-01-01"))
        self.firmware_version = self._info[service_type].get("FirmwareVersion", "")
        self.serial_number = self._info[service_type].get("SN", 0)
        self.mt_number = self._info[service_type].get("MT", 0)
        self.product = self._info[service_type].get("Product", "")

        self.device = DeviceApi(ip=self.ip, session=self._session, info=self._info[service_type])

    async def _get_plcnet_info(self):
        """ Get information from the devolo PlcNet API. """
        service_type = "_dvl-plcnetapi._tcp.local."
        try:
            await asyncio.wait_for(self._get_zeroconf_info(service_type=service_type), timeout=3)
        except asyncio.TimeoutError:
            return

        self.mac = self._info[service_type]['PlcMacAddress']
        self.technology = self._info[service_type].get("PlcTechnology", "")

        self.plcnet = PlcNetApi(ip=self.ip, session=self._session, info=self._info[service_type])

    async def _get_zeroconf_info(self, service_type: str):
        """ Browse for the desired mDNS service types and query them. """
        self._logger.debug("Browsing for %s", service_type)
        browser = ServiceBrowser(self._zeroconf, service_type, [self._state_change])
        while not self._info[service_type]:
            await asyncio.sleep(0.1)
        browser.cancel()

    async def _setup_device(self):
        """ Setup device. """
        self._session = httpx.AsyncClient()
        self._zeroconf = self._zeroconf_instance or Zeroconf()
        await asyncio.gather(self._get_device_info(), self._get_plcnet_info())
        if not self.device and not self.plcnet:
            raise DeviceNotFound(f"The device {self.ip} did not answer.")

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """ Evaluate the query result. """
        service_info = zeroconf.get_service_info(service_type, name)
        if service_info and state_change is ServiceStateChange.Added and \
                self.ip in [socket.inet_ntoa(address) for address in service_info.addresses]:
            self._logger.debug("Adding service info of %s", service_type)

            self._info[service_type]['Port'] = service_info.port

            # The answer is a byte string, that concatenates key-value pairs with their length as two byte hex value.
            total_length = len(service_info.text)
            offset = 0
            while offset < total_length:
                parsed_length, = struct.unpack_from("!B", service_info.text, offset)
                key_value = service_info.text[offset + 1:offset + 1 + parsed_length].decode("UTF-8").split("=")
                self._info[service_type][key_value[0]] = key_value[1]
                offset += parsed_length + 1
