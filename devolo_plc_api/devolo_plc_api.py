import time

from aiohttp import ClientSession
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from .wifi_network.wifi_network import WifiNetwork


def _on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
    """ Service handler for Zeroconf state changes. """
    if state_change is ServiceStateChange.Added:
        zeroconf.get_service_info(service_type, name)


class DevoloPlcApi(WifiNetwork):
    def __init__(self, ip: str, session: ClientSession, port: int):
        super().__init__(ip, session, port)


    def get_token(self):
        # Takes long time until the magic devices answer to zeroconf.
        zeroconf = Zeroconf()
        browser = ServiceBrowser(zeroconf, "_dvl._deviceapi._tcp.local.", handlers=[_on_service_state_change])
        start_time = time.time()
        while not time.time() > start_time + 10:
            time.sleep(8)
            for mdns_name in zeroconf.cache.entries():
                print(mdns_name)
        return



