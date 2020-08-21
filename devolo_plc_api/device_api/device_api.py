from .wifi_network.wifi_network import WifiNetwork
from ..helper.zeroconf import get_token


class DeviceApi:
    def __init__(self, ip, session):
        self.token, self.features = get_token(ip, "_dvl-deviceapi._tcp.local.")
        feature_mapping = {"wifi1": WifiNetwork}

        for feature in self.features:
            try:
                setattr(self, feature, feature_mapping.get(feature)(ip, session, 14791, self.token))
            except TypeError:
                continue