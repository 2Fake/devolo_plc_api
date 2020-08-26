import asyncio
import logging
import socket
import struct
from datetime import date

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

    def __init__(self, ip: str, zeroconf_instance: Zeroconf = None):
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

        self._info: dict = {"_dvl-plcnetapi._tcp.local.": {}, "_dvl-deviceapi._tcp.local.": {}}
        self._logger = logging.getLogger(self.__class__.__name__)
        self._zeroconf_instance = zeroconf_instance

    async def __aenter__(self):
        self._session = httpx.AsyncClient()
        self._zeroconf = self._zeroconf_instance or Zeroconf()
        loop = asyncio.get_running_loop()
        await loop.create_task(self._gather_apis())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._zeroconf_instance:
            self._zeroconf.close()
        await self._session.aclose()

    def __enter__(self):
        self._session = httpx.Client()
        self._zeroconf = self._zeroconf_instance or Zeroconf()
        asyncio.run(self._gather_apis())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._zeroconf_instance:
            self._zeroconf.close()
        self._session.close()


    async def _gather_apis(self):
        await asyncio.gather(self._get_device_info(), self._get_plcnet_info())

    async def _get_device_info(self):
        """ Get information from the device API. """
        service_type = "_dvl-deviceapi._tcp.local."
        try:
            await asyncio.wait_for(self._get_zeroconf_info(service_type=service_type), timeout=10)
        except asyncio.TimeoutError:
            raise DeviceNotFound(f"The device {self.ip} did not answer.") from None

        self.firmware_date = date.fromisoformat(self._info[service_type].get("FirmwareDate", "1970-01-01"))
        self.firmware_version = self._info[service_type].get("FirmwareVersion", "")
        self.serial_number = self._info[service_type].get("SN", 0)
        self.mt_number = self._info[service_type].get("MT", 0)
        self.product = self._info[service_type].get("Product", "")

        self.device = DeviceApi(ip=self.ip,
                                session=self._session,
                                path=self._info[service_type]['Path'],
                                version=self._info[service_type]['Version'],
                                features=self._info[service_type].get("Features", ""))

    async def _get_plcnet_info(self):
        """ Get information from the plcnet API. """
        service_type = "_dvl-plcnetapi._tcp.local."
        try:
            await asyncio.wait_for(self._get_zeroconf_info(service_type=service_type), timeout=10)
        except asyncio.TimeoutError:
            raise DeviceNotFound(f"The device {self.ip} did not answer.") from None

        self.mac = self._info[service_type].get("PlcMacAddress", "")
        self.technology = self._info[service_type].get("PlcTechnology", "")

        self.plcnet = PlcNetApi(ip=self.ip,
                                session=self._session,
                                path=self._info[service_type]['Path'],
                                version=self._info[service_type]['Version'])

    async def _get_zeroconf_info(self, service_type: str):
        """ Browse for the desired mDNS service types and query them. """
        self._logger.debug(f"Browsing for {service_type}")
        browser = ServiceBrowser(self._zeroconf, service_type, [self._state_change])
        while not self._info[service_type]:
            await asyncio.sleep(0.1)
        browser.cancel()

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """ Evaluate the query result. """
        service_info = zeroconf.get_service_info(service_type, name)
        if service_info and state_change is ServiceStateChange.Added and \
                self.ip in [socket.inet_ntoa(address) for address in service_info.addresses]:
            self._logger.debug(f"Adding service info of {service_type}")

            # The answer is a byte string, that concatenates key-value pairs with their length as two byte hex value.
            total_length = len(service_info.text)
            offset = 0
            while offset < total_length:
                parsed_length, = struct.unpack_from("!B", service_info.text, offset)
                key_value = service_info.text[offset + 1:offset + 1 + parsed_length].decode("UTF-8").split("=")
                self._info[service_type][key_value[0]] = key_value[1]
                offset += parsed_length + 1
