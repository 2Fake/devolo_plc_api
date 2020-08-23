from ..clients.protobuf import Protobuf
from . import devolo_idl_proto_deviceapi_wifinetwork_pb2
from ..exceptions.feature import FeatureNotSupported


class DeviceApi(Protobuf):
    def __init__(self, ip, session, path, version, features):
        self._ip = ip
        self._port = 14791
        self._session = session
        self._path = path
        self._version = version
        self._features = features.split(",")


    def _feature(feature):
        def feature_decorator(method):
            def wrapper(self):
                if feature in self._features:
                    return method(self)
                else:
                    raise FeatureNotSupported
            return wrapper
        return feature_decorator


    @_feature("wifi1")
    async def get_wifi_guest_access(self):
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        r = await self.get("WifiGuestAccessGet")
        wifi_guest_proto.ParseFromString(await r.read())
        return wifi_guest_proto
