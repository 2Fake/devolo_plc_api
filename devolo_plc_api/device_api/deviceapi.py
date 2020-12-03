from typing import Callable, Dict

from httpx import AsyncClient

from ..clients.protobuf import Protobuf
from ..exceptions.feature import FeatureNotSupported
from . import (devolo_idl_proto_deviceapi_ledsettings_pb2,
               devolo_idl_proto_deviceapi_updatefirmware_pb2,
               devolo_idl_proto_deviceapi_wifinetwork_pb2)


class DeviceApi(Protobuf):
    """
    Implementation of the devolo device API.

    :param ip: IP address of the device to communicate with
    :param session: HTTP client session
    :param info: Information collected from the mDNS query
    """

    def __init__(self, ip: str, session: AsyncClient, info: Dict):
        super().__init__()

        self._ip = ip
        # HC gateway has no Path, it has a path.
        self._path = info["properties"].get("Path") or info["properties"].get("path")
        self._port = info["port"]
        self._session = session
        self._user = "devolo"
        self._version = info["properties"]["Version"]

        features = info["properties"].get("Features", "")
        self.features = features.split(",") if features else ["reset", "update", "led", "intmtg"]
        self.password = ""

    def _feature(feature: str):  # type: ignore  # pylint: disable=no-self-argument
        """ Decorator to filter unsupported features before querying the device. """

        def feature_decorator(method: Callable):

            def wrapper(self, *args, **kwargs):
                if feature in self.features:
                    return method(self, *args, **kwargs)
                else:
                    raise FeatureNotSupported(f"The device does not support {method}.")

            return wrapper

        return feature_decorator

    @_feature("led")
    async def async_get_led_setting(self) -> dict:
        """
        Get LED setting asynchronously. This feature only works on devices, that announce the led feature.

        return: LED settings
        """
        self._logger.debug("Getting LED settings.")
        led_setting = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsGet()
        response = await self._async_get("LedSettingsGet")
        led_setting.FromString(await response.aread())  # pylint: disable=no-member
        return self._message_to_dict(led_setting)

    @_feature("led")
    async def async_set_led_setting(self, enable: bool) -> bool:
        """
        Set LED setting asynchronously. This feature only works on devices, that announce the led feature.

        :param enable: True to enable the LEDs, False to disable the LEDs
        :return: True, if LED state was successfully changed, otherwise False
        """
        self._logger.debug("Setting LED settings.")
        led_setting = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsSet()
        led_setting.state = int(not enable)
        query = await self._async_post("LedSettingsSet", content=led_setting.SerializeToString())
        response = devolo_idl_proto_deviceapi_ledsettings_pb2.LedSettingsSetResponse()
        response.FromString(await query.aread())  # pylint: disable=no-member
        return bool(not response.result)  # pylint: disable=no-member

    @_feature("update")
    async def async_check_firmware_available(self) -> dict:
        """
        Check asynchronously, if a firmware update is available for the device.

        :return: Result and new firmware version, if newer one is available
        """
        self._logger.debug("Checking for new firmware.")
        update_firmware_check = devolo_idl_proto_deviceapi_updatefirmware_pb2.UpdateFirmwareCheck()
        response = await self._async_get("UpdateFirmwareCheck")
        update_firmware_check.ParseFromString(await response.aread())
        return self._message_to_dict(update_firmware_check)

    @_feature("update")
    async def async_start_firmware_update(self) -> bool:
        """
        Start firmware update asynchronously, if a firmware update is available for the device. Important: The response does
        not tell you anything about the success of the update itself.

        :return: True, if the firmware update was started, False if there is no update
        """
        self._logger.debug("Updating firmware.")
        update_firmware = devolo_idl_proto_deviceapi_updatefirmware_pb2.UpdateFirmwareStart()
        response = await self._async_get("UpdateFirmwareStart")
        update_firmware.FromString(await response.aread())  # pylint: disable=no-member
        return bool(not update_firmware.result)  # pylint: disable=no-member

    @_feature("wifi1")
    async def async_get_wifi_connected_station(self) -> dict:
        """
        Get wifi stations connected to the device asynchronously. This feature only works on devices, that announce the wifi1
        feature.

        :return: All connected wifi stations including connection rate data
        """
        self._logger.debug("Getting connected wifi stations.")
        wifi_connected_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiConnectedStationsGet()
        response = await self._async_get("WifiConnectedStationsGet")
        wifi_connected_proto.ParseFromString(await response.aread())
        return self._message_to_dict(wifi_connected_proto)

    @_feature("wifi1")
    async def async_get_wifi_guest_access(self) -> dict:
        """
        Get details about wifi guest access asynchronously. This feature only works on devices, that announce the wifi1
        feature.

        :return: Details about the wifi guest access
        """
        self._logger.debug("Getting wifi guest access status.")
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        response = await self._async_get("WifiGuestAccessGet")
        wifi_guest_proto.ParseFromString(await response.aread())
        return self._message_to_dict(wifi_guest_proto)

    @_feature("wifi1")
    async def async_set_wifi_guest_access(self, enable: bool) -> bool:
        """
        Enable wifi guest access asynchronously. This feature only works on devices, that announce the wifi1 feature.

        :param enable: True to enable, False to disable wifi guest access
        :return: True, if the state of the wifi guest access was successfully changed, otherwise False
        """
        self._logger.debug("Setting wifi guest access status.")
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSet()
        wifi_guest_proto.enable = enable
        query = await self._async_post("WifiGuestAccessSet", content=wifi_guest_proto.SerializeToString())
        response = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessSetResponse()
        response.FromString(await query.aread())  # pylint: disable=no-member
        return bool(not response.result)  # pylint: disable=no-member

    @_feature("wifi1")
    async def async_get_wifi_neighbor_access_points(self) -> dict:
        """
        Get wifi access point in the neighborhood asynchronously. This feature only works on devices, that announce the wifi1
        feature.

        :return: Visible access points in the neighborhood including connection rate data
        """
        self._logger.debug("Getting neighbored access points.")
        wifi_neighbor_aps = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiNeighborAPsGet()
        response = await self._async_get("WifiNeighborAPsGet", timeout=15.0)
        wifi_neighbor_aps.ParseFromString(await response.aread())
        return self._message_to_dict(wifi_neighbor_aps)

    @_feature("wifi1")
    async def async_get_wifi_repeated_access_points(self):
        """
        Get repeated wifi access point asynchronously. This feature only works on repeater devices, that announce the wifi1
        feature.

        :return: Repeated access points in the neighborhood including connection rate data
        """
        self._logger.debug("Getting repeated access points.")
        wifi_connected_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiRepeatedAPsGet()
        response = await self._async_get("WifiRepeatedAPsGet")
        wifi_connected_proto.ParseFromString(await response.aread())
        return self._message_to_dict(wifi_connected_proto)

    @_feature("wifi1")
    async def async_start_wps(self):
        """
        Start WPS push button configuration.

        :return: True, if the WPS was successfully started, otherwise False
        """
        self._logger.debug("Starting WPS.")
        wps_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiWpsPbcStart()
        response = await self._async_get("WifiWpsPbcStart")
        wps_proto.FromString(await response.aread())  # pylint: disable=no-member
        return bool(not wps_proto.result)  # pylint: disable=no-member
