import logging
from typing import Callable

from httpx import Client

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

    def __init__(self, ip: str, session: Client, path: str, version: str, features: str, password: str):
        self._ip = ip
        self._port = 14791
        self._session = session
        self._path = path
        self._version = version
        self._features = features.split(",") if features else []
        self._logger = logging.getLogger(self.__class__.__name__)
        self._user = "devolo"
        self._password = password


    def _feature(feature: str, *args, **kwargs):  # type: ignore
        """ Decorator to filter unsupported features before querying the device. """
        def feature_decorator(method: Callable):
            def wrapper(self, *args, **kwargs):
                if feature in self._features:
                    return method(self, *args, **kwargs)
                else:
                    raise FeatureNotSupported(f"The device does not support {method}.")
            return wrapper
        return feature_decorator


    @_feature("wifi1")
    async def async_get_wifi_guest_access(self) -> dict:
        """ Get details about wifi guest access asynchronously. """
        self._logger.debug("Getting wifi guest access")
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        response = await self.async_get("WifiGuestAccessGet")
        wifi_guest_proto.ParseFromString(await response.aread())
        return wifi_guest_proto

    @_feature("wifi1")
    def get_wifi_guest_access(self) -> dict:
        """ Get details about wifi guest access synchronously. """
        self._logger.debug("Getting wifi guest access")
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        response = self.get("WifiGuestAccessGet")
        wifi_guest_proto.ParseFromString(response.content)
        return wifi_guest_proto

    @_feature("wifi1")
    async def async_set_wifi_guest_access(self, enable):
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSet()
        wifi_guest_proto.enable = enable
        r = await self.async_post("WifiGuestAccessSet", data=wifi_guest_proto.SerializeToString())
        wifi_guest_proto.ParseFromString(await r.aread())
        return wifi_guest_proto

    @_feature("wifi1")
    async def set_wifi_guest_access(self, enable):
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSet()
        wifi_guest_proto.enable = enable
        r = await self.async_post("WifiGuestAccessSet", data=wifi_guest_proto.SerializeToString())
        wifi_guest_proto.ParseFromString(await r.aread())
        return wifi_guest_proto
