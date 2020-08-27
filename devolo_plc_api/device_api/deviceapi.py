import logging
from typing import Callable

from httpx import Client

from ..clients.protobuf import Protobuf
from ..exceptions.feature import FeatureNotSupported
from . import devolo_idl_proto_deviceapi_wifinetwork_pb2
from . import devolo_idl_proto_deviceapi_ledsettings_pb2


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
        self._user = "devolo"
        self._password = password
        self._logger = logging.getLogger(self.__class__.__name__)


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


    @_feature("led")
    async def async_get_led_setting(self):
        """ Get LED setting asynchronously. """
        led_setting = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsGet()
        response = await self._async_get("LedSettingsGet")
        led_setting.FromString(await response.aread())
        return self._message_to_dict(message=led_setting)

    @_feature("led")
    def get_led_setting(self):
        """ Get LED setting synchronously. """
        led_setting = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsGet()
        response = self._get("LedSettingsGet")
        led_setting.FromString(response.read())
        return self._message_to_dict(message=led_setting)

    @_feature("led")
    async def async_set_led_setting(self, enable: bool) -> bool:
        """ Set LED setting asynchronously. """
        led_setting = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsSet()
        led_setting.state = int(not enable)
        query = await self._async_post("LedSettingsSet", data=led_setting.SerializeToString())
        response = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsSetResponse()
        response.FromString(await query.aread())
        return bool(not response.result)

    @_feature("led")
    def set_led_setting(self, enable: bool) -> bool:
        """ Set LED setting synchronously. """
        led_setting = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsSet()
        led_setting.state = int(not enable)
        query = self._post("LedSettingsSet", data=led_setting.SerializeToString())
        response = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsSetResponse()
        response.FromString(query.read())
        return bool(not response.result)

    @_feature("wifi1")
    async def async_get_wifi_connected_station(self) -> dict:
        """ Get wifi stations connected to the device asynchronously. """
        wifi_connected_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiConnectedStationsGet()
        response = await self._async_get("WifiConnectedStationsGet")
        wifi_connected_proto.FromString(await response.aread())
        return self._message_to_dict(wifi_connected_proto)

    @_feature("wifi1")
    def get_wifi_connected_station(self) -> dict:
        """ Get wifi stations connected to the device synchronously. """
        wifi_connected_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiConnectedStationsGet()
        response = self._get("WifiConnectedStationsGet")
        wifi_connected_proto.FromString(response.read())
        return self._message_to_dict(wifi_connected_proto)

    @_feature("wifi1")
    async def async_get_wifi_guest_access(self) -> dict:
        """ Get details about wifi guest access asynchronously. """
        self._logger.debug("Getting wifi guest access")
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        response = await self._async_get("WifiGuestAccessGet")
        wifi_guest_proto.FromString(await response.aread())
        return self._message_to_dict(wifi_guest_proto)

    @_feature("wifi1")
    def get_wifi_guest_access(self) -> dict:
        """ Get details about wifi guest access synchronously. """
        self._logger.debug("Getting wifi guest access")
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        response = self._get("WifiGuestAccessGet")
        wifi_guest_proto.FromString(response.read())
        return self._message_to_dict(wifi_guest_proto)

    @_feature("wifi1")
    async def async_set_wifi_guest_access(self, enable: bool) -> bool:
        """ Enable wifi guest access asynchronously. """
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSet()
        wifi_guest_proto.enable = enable
        query = await self._async_post("WifiGuestAccessSet", data=wifi_guest_proto.SerializeToString())
        response = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSetResponse()
        response.FromString(await query.aread())
        return bool(not response.result)

    @_feature("wifi1")
    def set_wifi_guest_access(self, enable: bool) -> bool:
        """ Enable wifi guest access synchronously. """
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSet()
        wifi_guest_proto.enable = enable
        query = self._post("WifiGuestAccessSet", data=wifi_guest_proto.SerializeToString())
        response = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSetResponse()
        response.FromString(query.read())
        return bool(not response.result)

    @_feature("wifi1")
    async def async_get_wifi_neighbor_access_points(self) -> dict:
        """ Get wifi access point in the neighborhood asynchronously. """
        wifi_neighbor_aps = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiNeighborAPsGet()
        response = await self._async_get("WifiNeighborAPsGet", timeout=15.0)
        wifi_neighbor_aps.FromString(await response.aread())
        return self._message_to_dict(wifi_neighbor_aps)

    @_feature("wifi1")
    def get_wifi_neighbor_access_points(self) -> dict:
        """ Get wifi access point in the neighborhood synchronously. """
        wifi_neighbor_aps = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiNeighborAPsGet()
        response = self._get("WifiNeighborAPsGet", timeout=15.0)
        wifi_neighbor_aps.FromString(response.read())
        return self._message_to_dict(wifi_neighbor_aps)

    @_feature("wifi1")
    async def async_get_wifi_repeated_access_points(self):
        wifi_connected_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiRepeatedAPsGet()
        response = await self._async_get("WifiRepeatedAPsGet")
        wifi_connected_proto.FromString(await response.aread())
        return self._message_to_dict(wifi_connected_proto)

    @_feature("wifi1")
    def get_wifi_repeated_access_points(self):
        wifi_connected_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiRepeatedAPsGet()
        response = self._get("WifiRepeatedAPsGet")
        wifi_connected_proto.FromString(response.read())
        return self._message_to_dict(wifi_connected_proto)
