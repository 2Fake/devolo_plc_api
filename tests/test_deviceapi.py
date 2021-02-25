import pytest
from google.protobuf.json_format import MessageToDict

from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsGet, LedSettingsSetResponse
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_updatefirmware_pb2 import UpdateFirmwareCheck, UpdateFirmwareStart
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_wifinetwork_pb2 import (WifiConnectedStationsGet,
                                                                                  WifiGuestAccessGet,
                                                                                  WifiGuestAccessSetResponse,
                                                                                  WifiNeighborAPsGet,
                                                                                  WifiRepeatedAPsGet,
                                                                                  WifiWpsPbcStart)
from devolo_plc_api.exceptions.feature import FeatureNotSupported


class TestDeviceApi:

    @pytest.mark.parametrize("feature", ["[]"])
    def test_unsupported_feature(self, device_api):
        with pytest.raises(FeatureNotSupported):
            device_api.get_led_setting()

    @pytest.mark.parametrize("feature", [""])
    def test_feature(self, device_api):
        assert device_api.features == ['reset', 'update', 'led', 'intmtg']

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["led"])
    async def test_async_get_led_setting(self, device_api, httpx_mock):
        led_setting_get = LedSettingsGet()
        httpx_mock.add_response(data=led_setting_get.SerializeToString())
        led_setting = await device_api.async_get_led_setting()
        assert led_setting == MessageToDict(led_setting_get,
                                            including_default_value_fields=True,
                                            preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["led"])
    def test_get_led_setting(self, device_api, httpx_mock):
        led_setting_get = LedSettingsGet()
        httpx_mock.add_response(data=led_setting_get.SerializeToString())
        led_setting = device_api.get_led_setting()
        assert led_setting == MessageToDict(led_setting_get,
                                            including_default_value_fields=True,
                                            preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["led"])
    async def test_async_set_led_setting(self, device_api, httpx_mock):
        led_setting_set = LedSettingsSetResponse()
        httpx_mock.add_response(data=led_setting_set.SerializeToString())
        assert await device_api.async_set_led_setting(True)

    @pytest.mark.parametrize("feature", ["led"])
    def test_set_led_setting(self, device_api, httpx_mock):
        led_setting_set = LedSettingsSetResponse()
        httpx_mock.add_response(data=led_setting_set.SerializeToString())
        assert device_api.set_led_setting(True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["update"])
    async def test_async_check_firmware_available(self, device_api, httpx_mock):
        firmware_available = UpdateFirmwareCheck()
        httpx_mock.add_response(data=firmware_available.SerializeToString())
        firmware = await device_api.async_check_firmware_available()
        assert firmware == MessageToDict(firmware_available,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["update"])
    def test_check_firmware_available(self, device_api, httpx_mock):
        firmware_available = UpdateFirmwareCheck()
        httpx_mock.add_response(data=firmware_available.SerializeToString())
        firmware = device_api.check_firmware_available()
        assert firmware == MessageToDict(firmware_available,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["update"])
    async def test_async_start_firmware_update(self, device_api, httpx_mock):
        firmware_update = UpdateFirmwareStart()
        httpx_mock.add_response(data=firmware_update.SerializeToString())
        assert await device_api.async_start_firmware_update()

    @pytest.mark.parametrize("feature", ["update"])
    def test_start_firmware_update(self, device_api, httpx_mock):
        firmware_update = UpdateFirmwareStart()
        httpx_mock.add_response(data=firmware_update.SerializeToString())
        assert device_api.start_firmware_update()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_connected_station(self, device_api, httpx_mock):
        wifi_connected_stations_get = WifiConnectedStationsGet()
        httpx_mock.add_response(data=wifi_connected_stations_get.SerializeToString())
        connected_stations = await device_api.async_get_wifi_connected_station()
        assert connected_stations == MessageToDict(wifi_connected_stations_get,
                                                   including_default_value_fields=True,
                                                   preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_connected_station(self, device_api, httpx_mock):
        wifi_connected_stations_get = WifiConnectedStationsGet()
        httpx_mock.add_response(data=wifi_connected_stations_get.SerializeToString())
        connected_stations = device_api.get_wifi_connected_station()
        assert connected_stations == MessageToDict(wifi_connected_stations_get,
                                                   including_default_value_fields=True,
                                                   preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_guest_access(self, device_api, httpx_mock):
        wifi_guest_access_get = WifiGuestAccessGet()
        httpx_mock.add_response(data=wifi_guest_access_get.SerializeToString())
        wifi_guest_access = await device_api.async_get_wifi_guest_access()
        assert wifi_guest_access == MessageToDict(wifi_guest_access_get,
                                                  including_default_value_fields=True,
                                                  preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_guest_access(self, device_api, httpx_mock):
        wifi_guest_access_get = WifiGuestAccessGet()
        httpx_mock.add_response(data=wifi_guest_access_get.SerializeToString())
        wifi_guest_access = device_api.get_wifi_guest_access()
        assert wifi_guest_access == MessageToDict(wifi_guest_access_get,
                                                  including_default_value_fields=True,
                                                  preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_set_wifi_guest_access(self, device_api, httpx_mock):
        wifi_guest_access_set = WifiGuestAccessSetResponse()
        httpx_mock.add_response(data=wifi_guest_access_set.SerializeToString())
        assert await device_api.async_set_wifi_guest_access(True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_set_wifi_guest_access(self, device_api, httpx_mock):
        wifi_guest_access_set = WifiGuestAccessSetResponse()
        httpx_mock.add_response(data=wifi_guest_access_set.SerializeToString())
        assert device_api.set_wifi_guest_access(True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_neighbor_access_points(self, device_api, httpx_mock):
        wifi_neighbor_accesspoints_get = WifiNeighborAPsGet()
        httpx_mock.add_response(data=wifi_neighbor_accesspoints_get.SerializeToString())
        wifi_neighbor_access_points = await device_api.async_get_wifi_neighbor_access_points()
        assert wifi_neighbor_access_points == MessageToDict(wifi_neighbor_accesspoints_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_neighbor_access_points(self, device_api, httpx_mock):
        wifi_neighbor_accesspoints_get = WifiNeighborAPsGet()
        httpx_mock.add_response(data=wifi_neighbor_accesspoints_get.SerializeToString())
        wifi_neighbor_access_points = device_api.get_wifi_neighbor_access_points()
        assert wifi_neighbor_access_points == MessageToDict(wifi_neighbor_accesspoints_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_repeated_access_points(self, device_api, httpx_mock):
        wifi_repeated_accesspoints_get = WifiRepeatedAPsGet()
        httpx_mock.add_response(data=wifi_repeated_accesspoints_get.SerializeToString())
        wifi_repeated_access_points = await device_api.async_get_wifi_repeated_access_points()
        assert wifi_repeated_access_points == MessageToDict(wifi_repeated_accesspoints_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_repeated_access_points(self, device_api, httpx_mock):
        wifi_repeated_accesspoints_get = WifiRepeatedAPsGet()
        httpx_mock.add_response(data=wifi_repeated_accesspoints_get.SerializeToString())
        wifi_repeated_access_points = device_api.get_wifi_repeated_access_points()
        assert wifi_repeated_access_points == MessageToDict(wifi_repeated_accesspoints_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_start_wps(self, device_api, httpx_mock):
        wps = WifiWpsPbcStart()
        httpx_mock.add_response(data=wps.SerializeToString())
        assert await device_api.async_start_wps()

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_start_wps(self, device_api, httpx_mock):
        wps = WifiWpsPbcStart()
        httpx_mock.add_response(data=wps.SerializeToString())
        assert device_api.start_wps()
