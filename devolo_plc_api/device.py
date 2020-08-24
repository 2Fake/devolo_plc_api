import asyncio
import logging
import socket
import struct
import time
from datetime import date

from aiohttp import ClientSession
from asyncinit import asyncinit
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from .device_api.deviceapi import DeviceApi
from .plcnet_api.plcnetapi import PlcNetApi


@asyncinit
class Device:
    """
    Representing object for your devolo PLC device. It stores all properties and functionalities discovered during setup.

    :param ip: IP address of the device to communicate with.
    :param session: HTTP client session
    """

    async def __init__(self, ip: str, session: ClientSession):
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

        self._zeroconf = Zeroconf()

        self._plc_info = {}
        self._info = {}
        self._logger = logging.getLogger(self.__class__.__name__)
        self._session = session

        loop = asyncio.get_running_loop()
        await loop.create_task(self.start())

        self._zeroconf.close()

        delattr(self, "_info")

    async def start(self):
        await asyncio.gather(self._get_device_info(), self._get_plcnet_info())

    async def _get_device_info(self):
        """ Get information from the device API. """
        await self._get_zeroconf_info(service_type="_dvl-deviceapi._tcp.local.")

        self.firmware_date = date.fromisoformat(self._info.get("FirmwareDate", "1970-01-01"))
        self.firmware_version = self._info['FirmwareVersion']
        self.serial_number = self._info['SN']
        self.mt_number = self._info['MT']
        self.product = self._info.get("Product", "")

        self.device = DeviceApi(ip=self.ip,
                                session=self._session,
                                path=self._info['Path'],
                                version=self._info['Version'],
                                features=self._info.get('Features'))

    async def _get_plcnet_info(self):
        """ Get information from the plcnet API. """
        await self._get_zeroconf_info(service_type="_dvl-plcnetapi._tcp.local.")

        self.mac = self._plc_info['PlcMacAddress']
        self.technology = self._plc_info['PlcTechnology']

        self.plcnet = PlcNetApi(ip=self.ip,
                                session=self._session,
                                path=self._plc_info['Path'],
                                version=self._plc_info['Version'])

    async def _get_zeroconf_info(self, service_type: str):
        """ Browse for the desired mDNS service types and query them. """
        self._logger.debug(f"Browsing for {service_type}")
        browser = ServiceBrowser(self._zeroconf, service_type, [self._state_change])
        start_time = time.time()
        while not time.time() > start_time + 10 and not (self._plc_info or self._info):
            await asyncio.sleep(1)
        browser.cancel()

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """ Evaluate the query result. """
        if state_change is ServiceStateChange.Added and \
            self.ip in [socket.inet_ntoa(address) for address in zeroconf.get_service_info(service_type, name).addresses]:

            self._logger.debug(f"Adding service info of {service_type}")
            service_info = zeroconf.get_service_info(service_type, name).text
            # The answer is a byte string, that concatenates key-value pairs with their length as two byte hex value.
            total_length = len(service_info)
            offset = 0
            while offset < total_length:
                parsed_length, = struct.unpack_from('!B', service_info, offset)
                key_value = service_info[offset + 1:offset + 1 + parsed_length].decode("UTF-8").split("=")
                if service_type == '_dvl-deviceapi._tcp.local.':
                    self._info[key_value[0]] = key_value[1]
                else:
                    self._plc_info[key_value[0]] = key_value[1]
                offset += parsed_length + 1
