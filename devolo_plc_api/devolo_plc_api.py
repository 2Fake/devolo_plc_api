from aiohttp import ClientSession

from .device_api.device_api import DeviceApi
from .plc_net_api.plc_net_api import PlcNetApi


class DevoloPlcApi():
    def __init__(self, ip: str, session: ClientSession):
        self.device_api = DeviceApi(ip, session)
        self.plc_net_api = PlcNetApi(ip, session)
