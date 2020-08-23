import socket
import struct
import time
from datetime import date

from aiohttp import ClientSession
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from .device_api.deviceapi import DeviceApi
from .plcnet_api.plcnetapi import PlcNetApi


class Device:
    """
    Representing object for your devolo PLC device. It stores all properties and functionallities discovered during setup.

    :param ip: IP address of the device to communicate with.
    :param session: HTTP client session
    """

    def __init__(self, ip: str, session: ClientSession):
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

        self._session = session

        self._zeroconf = Zeroconf()
        self._info = {}
        self._get_plcnet_info()
        self._info = {}
        self._get_device_info()
        self._zeroconf.close()

        delattr(self, "_info")


    def _get_device_info(self):
        """ Get information from the device API. """
        self._get_zeroconf_info(service_type="_dvl-deviceapi._tcp.local.")

        self.firmware_date = date.fromisoformat(self._info['FirmwareDate'])
        self.firmware_version = self._info['FirmwareVersion']
        self.serial_number = self._info['SN']
        self.mt_number = self._info['MT']
        self.product = self._info['Product']

        self.device = DeviceApi(ip=self.ip,
                                session=self._session,
                                path=self._info['Path'],
                                version=self._info['Version'],
                                features=self._info['Features'])

    def _get_plcnet_info(self):
        """ Get information from the plcnet API. """
        self._get_zeroconf_info(service_type="_dvl-plcnetapi._tcp.local.")

        self.mac = self._info['PlcMacAddress']
        self.technology = self._info['PlcTechnology']

        self.plcnet = PlcNetApi(ip=self.ip,
                                session=self._session,
                                path=self._info['Path'],
                                version=self._info['Version'])

    def _get_zeroconf_info(self, service_type: str):
        """ Browse for the desired mDNS service types and query them. """
        browser = ServiceBrowser(self._zeroconf, service_type, [self._state_change])
        start_time = time.time()
        while not time.time() > start_time + 10 and not self._info:
            time.sleep(0.1)
        browser.cancel()

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """ Evaluate the query result. """
        if state_change is ServiceStateChange.Added and \
                socket.inet_ntoa(zeroconf.get_service_info(service_type, name).address) == self.ip:
            service_info = zeroconf.get_service_info(service_type, name).text

            # The answer is a byte string, that concatenates key-value pairs with their length as two byte hex value.
            total_length = len(service_info)
            offset = 0
            while offset < total_length:
                parsed_length, = struct.unpack_from('!B', service_info, offset)
                key_value = service_info[offset + 1:offset + 1 + parsed_length].decode("UTF-8").split("=")
                self._info[key_value[0]] = key_value[1]
                offset += parsed_length + 1
