"""Implementation of the devolo device API."""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Callable, TypeVar

from devolo_plc_api.clients import Protobuf
from devolo_plc_api.exceptions import FeatureNotSupported

from .factoryreset_pb2 import FactoryResetStart
from .ledsettings_pb2 import LedSettingsGet, LedSettingsSet, LedSettingsSetResponse
from .multiap_pb2 import WifiMultiApGetResponse
from .restart_pb2 import RestartResponse, UptimeGetResponse
from .support_pb2 import SupportInfoDump, SupportInfoDumpResponse
from .updatefirmware_pb2 import UpdateFirmwareCheck, UpdateFirmwareStart
from .wifinetwork_pb2 import (
    WifiConnectedStationsGet,
    WifiGuestAccessGet,
    WifiGuestAccessSet,
    WifiGuestAccessSetResponse,
    WifiNeighborAPsGet,
    WifiRepeatedAPsGet,
    WifiRepeaterWpsClonePbcStart,
    WifiResult,
    WifiWpsPbcStart,
)

if TYPE_CHECKING:
    from httpx import AsyncClient
    from typing_extensions import Concatenate, ParamSpec

    from devolo_plc_api.zeroconf import ZeroconfServiceInfo

    _ReturnT = TypeVar("_ReturnT")
    _P = ParamSpec("_P")


LONG_RUNNING = 30.0


def _feature(
    feature: str,
) -> Callable[[Callable[Concatenate[DeviceApi, _P], _ReturnT]], Callable[Concatenate[DeviceApi, _P], _ReturnT]]:
    """Filter unsupported features before querying the device."""

    def feature_decorator(method: Callable[Concatenate[DeviceApi, _P], _ReturnT]) -> Callable[..., _ReturnT]:
        @functools.wraps(method)
        def wrapper(deviceapi: DeviceApi, *args: _P.args, **kwargs: _P.kwargs) -> _ReturnT:
            if feature in deviceapi.features:
                return method(deviceapi, *args, **kwargs)
            raise FeatureNotSupported(method.__name__)

        return wrapper

    return feature_decorator


class DeviceApi(Protobuf):
    """
    Implementation of the devolo device API.

    :param ip: IP address of the device to communicate with
    :param session: HTTP client session
    :param info: Information collected from the mDNS query
    """

    def __init__(self, ip: str, session: AsyncClient, info: ZeroconfServiceInfo) -> None:
        """Initialize the device API."""
        super().__init__()

        self._ip = ip
        # HC gateway has no Path, it has a path.
        self._path = info.properties.get("Path") or info.properties.get("path")
        self._port = info.port
        self._session = session
        self._user = "devolo"
        self._version = info.properties["Version"]

        features: str = info.properties.get("Features", "")
        self.features = features.split(",") if features else ["reset", "update", "led", "intmtg"]
        self.password = ""

    @_feature("led")
    async def async_get_led_setting(self) -> bool:
        """
        Get LED setting asynchronously. This feature only works on devices, that announce the led feature.

        return: LED settings
        """
        self._logger.debug("Getting LED settings.")
        led_setting = LedSettingsGet()
        response = await self._async_get("LedSettingsGet")
        led_setting.ParseFromString(await response.aread())
        return led_setting.state == led_setting.LED_ON

    @_feature("led")
    async def async_set_led_setting(self, enable: bool) -> bool:
        """
        Set LED setting asynchronously. This feature only works on devices, that announce the led feature.

        :param enable: True to enable the LEDs, False to disable the LEDs
        :return: True, if LED state was successfully changed, otherwise False
        """
        self._logger.debug("Setting LED settings.")
        led_setting = LedSettingsSet()
        led_setting.state = led_setting.LED_ON if enable else led_setting.LED_OFF
        query = await self._async_post("LedSettingsSet", content=led_setting.SerializeToString())
        response = LedSettingsSetResponse()
        response.ParseFromString(await query.aread())
        return response.result == response.SUCCESS

    @_feature("multiap")
    async def async_get_wifi_multi_ap(self) -> WifiMultiApGetResponse:
        """
        Get MultiAP details asynchronously. This feature only works on devices, that announce the multiap feature.

        return: MultiAP details
        """
        self._logger.debug("Getting MultiAP details.")
        query = await self._async_get("WifiMultiApGet")
        response = WifiMultiApGetResponse()
        response.ParseFromString(await query.aread())
        return response

    @_feature("repeater0")
    async def async_get_wifi_repeated_access_points(self) -> list[WifiRepeatedAPsGet.RepeatedAPInfo]:
        """
        Get repeated wifi access point asynchronously. This feature only works on repeater devices, that announce the
        repeater0 feature.

        :return: Repeated access points in the neighborhood including connection rate data
        """
        self._logger.debug("Getting repeated access points.")
        repeated_aps = WifiRepeatedAPsGet()
        response = await self._async_get("WifiRepeatedAPsGet")
        repeated_aps.ParseFromString(await response.aread())
        return list(repeated_aps.repeated_aps)

    @_feature("repeater0")
    async def async_start_wps_clone(self) -> bool:
        """
        Start WPS clone mode. This feature only works on repeater devices, that announce the repeater0 feature.

        :return: True, if the wifi settings were successfully cloned, otherwise False
        """
        self._logger.debug("Starting WPS clone.")
        wps_clone = WifiRepeaterWpsClonePbcStart()
        response = await self._async_get("WifiRepeaterWpsClonePbcStart")
        wps_clone.ParseFromString(await response.aread())
        return wps_clone.result == WifiResult.WIFI_SUCCESS

    @_feature("reset")
    async def async_factory_reset(self) -> bool:
        """
        Factory-reset the device. This feature only works on devices, that announce the reset feature.

        :return: True if reset is started, otherwise False
        """
        self._logger.debug("Resetting the device.")
        reset = FactoryResetStart()
        response = await self._async_get("FactoryResetStart")
        reset.ParseFromString(await response.aread())
        return reset.result == reset.SUCCESS

    @_feature("restart")
    async def async_restart(self) -> bool:
        """
        Restart the device. This feature only works on devices, that announce the restart feature.

        :return: True if restart is started, otherwise False
        """
        self._logger.debug("Restarting the device.")
        query = await self._async_post("Restart", content=b"")
        response = RestartResponse()
        response.ParseFromString(await query.aread())
        return response.result == response.SUCCESS

    @_feature("restart")
    async def async_uptime(self) -> int:
        """
        Get the uptime of the device. This feature only works on devices, that announce the restart feature. It can only be
        used as a strict monotonically increasing number and therefore has no unit.

        :return: The uptime without unit
        """
        self._logger.debug("Get uptime.")
        uptime = UptimeGetResponse()
        response = await self._async_get("UptimeGet")
        uptime.ParseFromString(await response.aread())
        return uptime.uptime

    @_feature("support")
    async def async_get_support_info(self) -> SupportInfoDump:
        """
        Get support info from the device. This feature only works on devices, that announce the support feature.

        :return: The support info
        """
        self._logger.debug("Get uptime.")
        support_info = SupportInfoDumpResponse()
        response = await self._async_get("SupportInfoDump", timeout=LONG_RUNNING)
        support_info.ParseFromString(await response.aread())
        return support_info.info

    @_feature("update")
    async def async_check_firmware_available(self) -> UpdateFirmwareCheck:
        """
        Check asynchronously, if a firmware update is available for the device.

        :return: Result and new firmware version, if newer one is available
        """
        self._logger.debug("Checking for new firmware.")
        update_firmware_check = UpdateFirmwareCheck()
        response = await self._async_get("UpdateFirmwareCheck", timeout=LONG_RUNNING)
        update_firmware_check.ParseFromString(await response.aread())
        return update_firmware_check

    @_feature("update")
    async def async_start_firmware_update(self) -> bool:
        """
        Start firmware update asynchronously, if a firmware update is available for the device. Important: The response does
        not tell you anything about the success of the update itself.

        :return: True, if the firmware update was started, False if there is no update
        """
        self._logger.debug("Updating firmware.")
        update_firmware = UpdateFirmwareStart()
        query = await self._async_get("UpdateFirmwareStart")
        update_firmware.ParseFromString(await query.aread())
        return update_firmware.result == update_firmware.UPDATE_STARTED

    @_feature("wifi1")
    async def async_get_wifi_connected_station(self) -> list[WifiConnectedStationsGet.ConnectedStationInfo]:
        """
        Get wifi stations connected to the device asynchronously. This feature only works on devices, that announce the wifi1
        feature.

        :return: All connected wifi stations including connection rate data
        """
        self._logger.debug("Getting connected wifi stations.")
        wifi_connected = WifiConnectedStationsGet()
        response = await self._async_get("WifiConnectedStationsGet")
        wifi_connected.ParseFromString(await response.aread())
        return list(wifi_connected.connected_stations)

    @_feature("wifi1")
    async def async_get_wifi_guest_access(self) -> WifiGuestAccessGet:
        """
        Get details about wifi guest access asynchronously. This feature only works on devices, that announce the wifi1
        feature.

        :return: Details about the wifi guest access
        """
        self._logger.debug("Getting wifi guest access status.")
        wifi_guest = WifiGuestAccessGet()
        response = await self._async_get("WifiGuestAccessGet")
        wifi_guest.ParseFromString(await response.aread())
        return wifi_guest

    @_feature("wifi1")
    async def async_set_wifi_guest_access(self, enable: bool, duration: int = 0) -> bool:
        """
        Enable wifi guest access asynchronously. This feature only works on devices, that announce the wifi1 feature.

        :param enable: True to enable, False to disable wifi guest access
        :param duration: Duration in minutes to enable the guest wifi. 0 is infinite.
        :return: True, if the state of the wifi guest access was successfully changed, otherwise False
        """
        self._logger.debug("Setting wifi guest access status.")
        wifi_guest = WifiGuestAccessSet()
        wifi_guest.enable = enable
        wifi_guest.duration = duration
        query = await self._async_post("WifiGuestAccessSet", content=wifi_guest.SerializeToString())
        response = WifiGuestAccessSetResponse()
        response.ParseFromString(await query.aread())
        return response.result == WifiResult.WIFI_SUCCESS

    @_feature("wifi1")
    async def async_get_wifi_neighbor_access_points(self) -> list[WifiNeighborAPsGet.NeighborAPInfo]:
        """
        Get wifi access point in the neighborhood asynchronously. This feature only works on devices, that announce the wifi1
        feature.

        :return: Visible access points in the neighborhood including connection rate data
        """
        self._logger.debug("Getting neighbored access points.")
        wifi_neighbor_aps = WifiNeighborAPsGet()
        response = await self._async_get("WifiNeighborAPsGet", timeout=LONG_RUNNING)
        wifi_neighbor_aps.ParseFromString(await response.aread())
        return list(wifi_neighbor_aps.neighbor_aps)

    @_feature("wifi1")
    async def async_start_wps(self) -> bool:
        """
        Start WPS push button configuration.

        :return: True, if the WPS was successfully started, otherwise False
        """
        self._logger.debug("Starting WPS.")
        wps = WifiWpsPbcStart()
        response = await self._async_get("WifiWpsPbcStart")
        wps.ParseFromString(await response.aread())
        return wps.result == WifiResult.WIFI_SUCCESS
