from unittest.mock import patch

import pytest
from google.protobuf.json_format import MessageToDict

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsGet, LedSettingsSetResponse
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_wifinetwork_pb2 import (
    WifiConnectedStationsGet, WifiGuestAccessGet, WifiGuestAccessSetResponse, WifiNeighborAPsGet, WifiRepeatedAPsGet,
    WifiWpsPbcStart)
from devolo_plc_api.exceptions.feature import FeatureNotSupported
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_updatefirmware_pb2 import UpdateFirmwareCheck, UpdateFirmwareStart


class TestDeviceApi:

    @pytest.mark.parametrize("feature", ["[]"])
    def test_unsupported_feature(self, device_api_sync):
        with pytest.raises(FeatureNotSupported):
            device_api_sync.get_led_setting()

    @pytest.mark.parametrize("feature", [""])
    def test_feature(self, device_api_sync):
        assert device_api_sync.features == ['reset', 'update', 'led', 'intmtg']

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["led"])
    async def test_async_get_led_setting(self, device_api_async):
        led_setting_get = LedSettingsGet()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=led_setting_get.SerializeToString())):
            led_setting = await device_api_async.async_get_led_setting()
            assert led_setting == MessageToDict(led_setting_get,
                                                including_default_value_fields=True,
                                                preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["led"])
    def test_get_led_setting(self, device_api_sync):
        led_setting_get = LedSettingsGet()
        with patch("httpx.Response.read", return_value=led_setting_get.SerializeToString()):
            led_setting = device_api_sync.get_led_setting()
            assert led_setting == MessageToDict(led_setting_get,
                                                including_default_value_fields=True,
                                                preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["led"])
    async def test_async_set_led_setting(self, device_api_async):
        led_setting_set = LedSettingsSetResponse()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=led_setting_set.SerializeToString())):
            assert await device_api_async.async_set_led_setting(True)

    @pytest.mark.parametrize("feature", ["led"])
    def test_set_led_setting(self, device_api_sync):
        led_setting_set = LedSettingsSetResponse()
        with patch("httpx.Response.read", return_value=led_setting_set.SerializeToString()):
            assert device_api_sync.set_led_setting(True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["update"])
    async def test_async_check_firmware_available(self, device_api_async):
        firmware_available = UpdateFirmwareCheck()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=firmware_available.SerializeToString())):
            firmware = await device_api_async.async_check_firmware_available()
            assert firmware == MessageToDict(firmware_available,
                                             including_default_value_fields=True,
                                             preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["update"])
    def test_check_firmware_available(self, device_api_sync):
        firmware_available = UpdateFirmwareCheck()
        with patch("httpx.Response.read", return_value=firmware_available.SerializeToString()):
            firmware = device_api_sync.check_firmware_available()
            assert firmware == MessageToDict(firmware_available,
                                             including_default_value_fields=True,
                                             preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["update"])
    async def test_async_start_firmware_update(self, device_api_async):
        firmware_update = UpdateFirmwareStart()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=firmware_update.SerializeToString())):
            assert await device_api_async.async_start_firmware_update()

    @pytest.mark.parametrize("feature", ["update"])
    def test_start_firmware_update(self, device_api_sync):
        firmware_update = UpdateFirmwareStart()
        with patch("httpx.Response.read", return_value=firmware_update.SerializeToString()):
            assert device_api_sync.start_firmware_update()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_connected_station(self, device_api_async):
        wifi_connected_stations_get = WifiConnectedStationsGet()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_connected_stations_get.SerializeToString())):
            connected_stations = await device_api_async.async_get_wifi_connected_station()
            assert connected_stations == MessageToDict(wifi_connected_stations_get,
                                                       including_default_value_fields=True,
                                                       preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_connected_station(self, device_api_sync):
        wifi_connected_stations_get = WifiConnectedStationsGet()
        with patch("httpx.Response.read", return_value=wifi_connected_stations_get.SerializeToString()):
            connected_stations = device_api_sync.get_wifi_connected_station()
            assert connected_stations == MessageToDict(wifi_connected_stations_get,
                                                       including_default_value_fields=True,
                                                       preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_guest_access(self, device_api_async):
        wifi_guest_access_get = WifiGuestAccessGet()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_guest_access_get.SerializeToString())):
            wifi_guest_access = await device_api_async.async_get_wifi_guest_access()
            assert wifi_guest_access == MessageToDict(wifi_guest_access_get,
                                                      including_default_value_fields=True,
                                                      preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_guest_access(self, device_api_sync):
        wifi_guest_access_get = WifiGuestAccessGet()
        with patch("httpx.Response.read", return_value=wifi_guest_access_get.SerializeToString()):
            wifi_guest_access = device_api_sync.get_wifi_guest_access()
            assert wifi_guest_access == MessageToDict(wifi_guest_access_get,
                                                      including_default_value_fields=True,
                                                      preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_set_wifi_guest_access(self, device_api_async):
        wifi_guest_access_set = WifiGuestAccessSetResponse()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_guest_access_set.SerializeToString())):
            assert await device_api_async.async_set_wifi_guest_access(True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_set_wifi_guest_access(self, device_api_sync):
        wifi_guest_access_set = WifiGuestAccessSetResponse()
        with patch("httpx.Response.read", return_value=wifi_guest_access_set.SerializeToString()):
            assert device_api_sync.set_wifi_guest_access(True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_neighbor_access_points(self, device_api_async):
        wifi_neighbor_accesspoints_get = WifiNeighborAPsGet()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_neighbor_accesspoints_get.SerializeToString())):
            wifi_neighbor_access_points = await device_api_async.async_get_wifi_neighbor_access_points()
            assert wifi_neighbor_access_points == MessageToDict(wifi_neighbor_accesspoints_get,
                                                                including_default_value_fields=True,
                                                                preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_neighbor_access_points(self, device_api_sync):
        wifi_neighbor_access_points_get = WifiNeighborAPsGet()

        with patch("httpx.Response.read", return_value=wifi_neighbor_access_points_get.SerializeToString()):
            wifi_neighbor_access_points = device_api_sync.get_wifi_neighbor_access_points()
            assert wifi_neighbor_access_points == MessageToDict(wifi_neighbor_access_points_get,
                                                                including_default_value_fields=True,
                                                                preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_repeated_access_points(self, device_api_async):
        wifi_repeated_accesspoints_get = WifiRepeatedAPsGet()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_repeated_accesspoints_get.SerializeToString())):
            wifi_repeated_access_points = await device_api_async.async_get_wifi_repeated_access_points()
            assert wifi_repeated_access_points == MessageToDict(wifi_repeated_accesspoints_get,
                                                                including_default_value_fields=True,
                                                                preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_repeated_access_points(self, device_api_sync):
        wifi_repeated_access_points_get = WifiRepeatedAPsGet()
        with patch("httpx.Response.read", return_value=wifi_repeated_access_points_get.SerializeToString()):
            wifi_repeated_access_points = device_api_sync.get_wifi_repeated_access_points()
            assert wifi_repeated_access_points == MessageToDict(wifi_repeated_access_points_get,
                                                                including_default_value_fields=True,
                                                                preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_start_wps(self, device_api_async):
        wps = WifiWpsPbcStart()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=wps.SerializeToString())):
            assert await device_api_async.async_start_wps()

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_start_wps(self, device_api_sync):
        wps = WifiWpsPbcStart()
        with patch("httpx.Response.read", return_value=wps.SerializeToString()):
            assert device_api_sync.start_wps()
