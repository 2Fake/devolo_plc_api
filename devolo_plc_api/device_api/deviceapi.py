import logging
from typing import Callable

from aiohttp import ClientSession

from ..clients.protobuf import Protobuf
from ..exceptions.feature import FeatureNotSupported
from . import devolo_idl_proto_deviceapi_wifinetwork_pb2


class DeviceApi(Protobuf):
    """
    Implementation of the devolo device API.

    :param ip: IP address of the device to communicate with
    :param session: HTTP client session
    :param path: Path to send queries to
    :param version: Version of the API to use
    :param features: Feature, the device has
    """

    def __init__(self, ip: str, session: ClientSession, path: str, version: str, features: str):
        self._ip = ip
        self._port = 14791
        self._session = session
        self._path = path
        self._version = version
        self._features = features.split(",")
        self._logger = logging.getLogger(self.__class__.__name__)


    def _feature(feature: str):
        """ Decorator to filter unsupported features before querying the device. """
        def feature_decorator(method: Callable):
            def wrapper(self):
                if feature in self._features:
                    return method(self)
                else:
                    raise FeatureNotSupported(f"The device does not support {method}.")
            return wrapper
        return feature_decorator


    @_feature("wifi1")
    async def get_wifi_guest_access(self) -> dict:
        """ Get details about wifi guest access. """
        self._logger.debug("Getting wifi guest access")
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        r = await self.get("WifiGuestAccessGet")
        wifi_guest_proto.ParseFromString(await r.read())
        return wifi_guest_proto
