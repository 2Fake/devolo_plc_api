import re
import socket
import time
from datetime import date

from aiohttp import ClientSession
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from .plcnet_api.plcnetapi import PlcNetApi
from .device_api.deviceapi import DeviceApi


class Device:
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
        self._info = None
        self._get_plcnet_info()
        self._info = None
        self._get_device_info()
        self._zeroconf.close()

        delattr(self, "_info")


    def _get_plcnet_info(self):
        self._get_zeroconf_info(service_type="_dvl-plcnetapi._tcp.local.")

        info = dict(s.split('=') for s in [x for x in self._info if x])
        self.mac = info['PlcMacAddress']
        self.technology = info['PlcTechnology']

        self.plcnet = PlcNetApi(ip=self.ip,
                                session=self._session,
                                path=info['Path'],
                                version=info['Version'])

    def _get_device_info(self):
        self._get_zeroconf_info(service_type="_dvl-deviceapi._tcp.local.")

        info = dict(s.split('=') for s in [x for x in self._info if x])
        self.firmware_date = date.fromisoformat(info['FirmwareDate'])
        self.firmware_version = info['FirmwareVersion']
        self.serial_number = info['SN']
        self.mt_number = info['MT']
        self.product = info['Product']

        self.device = DeviceApi(ip=self.ip,
                                session=self._session,
                                path=info['Path'],
                                version=info['Version'],
                                features=info['Features'])

    def _get_zeroconf_info(self, service_type: str):
        browser = ServiceBrowser(self._zeroconf, service_type, [self._state_change])
        start_time = time.time()
        while not time.time() > start_time + 10 and self._info is None:
            time.sleep(0.1)
        browser.cancel()

    def _state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        if state_change is ServiceStateChange.Added and \
                socket.inet_ntoa(zeroconf.get_service_info(service_type, name).address) == self.ip:
            service_info = zeroconf.get_service_info(service_type, name).text.decode("UTF-8")
            self._info = re.split("[^ -~]+", service_info.replace("PS=", ""))
