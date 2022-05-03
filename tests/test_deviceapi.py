"""Test communicating with a the device API."""
import pytest
from google.protobuf.json_format import MessageToDict
from pytest_httpx import HTTPXMock

from devolo_plc_api.device_api import DeviceApi
from devolo_plc_api.device_api.factoryreset_pb2 import FactoryResetStart
from devolo_plc_api.device_api.ledsettings_pb2 import LedSettingsGet, LedSettingsSetResponse
from devolo_plc_api.device_api.restart_pb2 import RestartResponse, UptimeGetResponse
from devolo_plc_api.device_api.updatefirmware_pb2 import UpdateFirmwareCheck, UpdateFirmwareStart
from devolo_plc_api.device_api.wifinetwork_pb2 import (
    WifiConnectedStationsGet,
    WifiGuestAccessGet,
    WifiGuestAccessSetResponse,
    WifiNeighborAPsGet,
    WifiRepeatedAPsGet,
    WifiRepeaterWpsClonePbcStart,
    WifiWpsPbcStart,
)
from devolo_plc_api.exceptions.feature import FeatureNotSupported


class TestDeviceApi:
    """Test devolo_plc_api.device_api.deviceapi.DeviceApi class."""

    @pytest.mark.parametrize("feature", ["[]"])
    def test_unsupported_feature(self, device_api: DeviceApi):
        """Test raising on using unsupported feature."""
        with pytest.raises(FeatureNotSupported):
            device_api.get_led_setting()

    @pytest.mark.parametrize("feature", [""])
    def test_feature(self, device_api: DeviceApi):
        """Test list of default features."""
        assert device_api.features == ["reset", "update", "led", "intmtg"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["led"])
    async def test_async_get_led_setting(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting LED settings asynchronously."""
        led_setting_get = LedSettingsGet()
        httpx_mock.add_response(content=led_setting_get.SerializeToString())
        led_setting = await device_api.async_get_led_setting()
        assert led_setting == MessageToDict(
            led_setting_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.parametrize("feature", ["led"])
    def test_get_led_setting(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting LED settings synchronously."""
        led_setting_get = LedSettingsGet()
        httpx_mock.add_response(content=led_setting_get.SerializeToString())
        led_setting = device_api.get_led_setting()
        assert led_setting == MessageToDict(
            led_setting_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["led"])
    async def test_async_set_led_setting(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test setting LED settings asynchronously."""
        led_setting_set = LedSettingsSetResponse()
        httpx_mock.add_response(content=led_setting_set.SerializeToString())
        assert await device_api.async_set_led_setting(True)

    @pytest.mark.parametrize("feature", ["led"])
    def test_set_led_setting(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test setting LED settings synchronously."""
        led_setting_set = LedSettingsSetResponse()
        httpx_mock.add_response(content=led_setting_set.SerializeToString())
        assert device_api.set_led_setting(True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["repeater0"])
    async def test_async_get_wifi_repeated_access_points(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting AP settings asynchronously."""
        wifi_repeated_accesspoints_get = WifiRepeatedAPsGet()
        httpx_mock.add_response(content=wifi_repeated_accesspoints_get.SerializeToString())
        wifi_repeated_access_points = await device_api.async_get_wifi_repeated_access_points()
        assert wifi_repeated_access_points == MessageToDict(
            wifi_repeated_accesspoints_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.parametrize("feature", ["repeater0"])
    def test_get_wifi_repeated_access_points(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting AP settings synchronously."""
        wifi_repeated_accesspoints_get = WifiRepeatedAPsGet()
        httpx_mock.add_response(content=wifi_repeated_accesspoints_get.SerializeToString())
        wifi_repeated_access_points = device_api.get_wifi_repeated_access_points()
        assert wifi_repeated_access_points == MessageToDict(
            wifi_repeated_accesspoints_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["repeater0"])
    async def test_async_start_wps_clone(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test starting WPS clone mode asynchronously."""
        wps = WifiRepeaterWpsClonePbcStart()
        httpx_mock.add_response(content=wps.SerializeToString())
        assert await device_api.async_start_wps_clone()

    @pytest.mark.parametrize("feature", ["repeater0"])
    def test_start_wps_clone(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test starting WPS clone mode synchronously."""
        wps = WifiRepeaterWpsClonePbcStart()
        httpx_mock.add_response(content=wps.SerializeToString())
        assert device_api.start_wps_clone()

    @pytest.mark.parametrize("feature", ["reset"])
    async def test_async_factory_reset(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test factory reset asynchronously."""
        reset = FactoryResetStart()
        httpx_mock.add_response(content=reset.SerializeToString())
        assert await device_api.async_factory_reset()

    @pytest.mark.parametrize("feature", ["reset"])
    def test_factory_reset(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test factory reset synchronously."""
        reset = FactoryResetStart()
        httpx_mock.add_response(content=reset.SerializeToString())
        assert device_api.factory_reset()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["restart"])
    async def test_async_restart(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test restarting a device asynchronously."""
        restart = RestartResponse()
        httpx_mock.add_response(content=restart.SerializeToString())
        assert await device_api.async_restart()

    @pytest.mark.parametrize("feature", ["restart"])
    def test_restart(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test restarting a device synchronously."""
        restart = RestartResponse()
        httpx_mock.add_response(content=restart.SerializeToString())
        assert device_api.restart()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["restart"])
    async def test_async_uptime(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting a device's update asynchronously."""
        uptime = UptimeGetResponse()
        httpx_mock.add_response(content=uptime.SerializeToString())
        assert await device_api.async_uptime() == 0

    @pytest.mark.parametrize("feature", ["restart"])
    def test_uptime(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting a device's update synchronously."""
        uptime = UptimeGetResponse()
        httpx_mock.add_response(content=uptime.SerializeToString())
        assert device_api.uptime() == 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["update"])
    async def test_async_check_firmware_available(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test checking for firmware updates asynchronously."""
        firmware_available = UpdateFirmwareCheck()
        httpx_mock.add_response(content=firmware_available.SerializeToString())
        firmware = await device_api.async_check_firmware_available()
        assert firmware == MessageToDict(
            firmware_available, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.parametrize("feature", ["update"])
    def test_check_firmware_available(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test checking for firmware updates synchronously."""
        firmware_available = UpdateFirmwareCheck()
        httpx_mock.add_response(content=firmware_available.SerializeToString())
        firmware = device_api.check_firmware_available()
        assert firmware == MessageToDict(
            firmware_available, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["update"])
    async def test_async_start_firmware_update(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test firmware update asynchronously."""
        firmware_update = UpdateFirmwareStart()
        httpx_mock.add_response(content=firmware_update.SerializeToString())
        assert await device_api.async_start_firmware_update()

    @pytest.mark.parametrize("feature", ["update"])
    def test_start_firmware_update(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test firmware update synchronously."""
        firmware_update = UpdateFirmwareStart()
        httpx_mock.add_response(content=firmware_update.SerializeToString())
        assert device_api.start_firmware_update()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_connected_station(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting connected wifi clients asynchronously."""
        wifi_connected_stations_get = WifiConnectedStationsGet()
        httpx_mock.add_response(content=wifi_connected_stations_get.SerializeToString())
        connected_stations = await device_api.async_get_wifi_connected_station()
        assert connected_stations == MessageToDict(
            wifi_connected_stations_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_connected_station(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting connected wifi clients synchronously."""
        wifi_connected_stations_get = WifiConnectedStationsGet()
        httpx_mock.add_response(content=wifi_connected_stations_get.SerializeToString())
        connected_stations = device_api.get_wifi_connected_station()
        assert connected_stations == MessageToDict(
            wifi_connected_stations_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_guest_access(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting wifi guest access status asynchronously."""
        wifi_guest_access_get = WifiGuestAccessGet()
        httpx_mock.add_response(content=wifi_guest_access_get.SerializeToString())
        wifi_guest_access = await device_api.async_get_wifi_guest_access()
        assert wifi_guest_access == MessageToDict(
            wifi_guest_access_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_guest_access(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting wifi guest access status synchronously."""
        wifi_guest_access_get = WifiGuestAccessGet()
        httpx_mock.add_response(content=wifi_guest_access_get.SerializeToString())
        wifi_guest_access = device_api.get_wifi_guest_access()
        assert wifi_guest_access == MessageToDict(
            wifi_guest_access_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_set_wifi_guest_access(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test setting wifi guest access status asynchronously."""
        wifi_guest_access_set = WifiGuestAccessSetResponse()
        httpx_mock.add_response(content=wifi_guest_access_set.SerializeToString())
        assert await device_api.async_set_wifi_guest_access(True)

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_set_wifi_guest_access(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test setting wifi guest access status synchronously."""
        wifi_guest_access_set = WifiGuestAccessSetResponse()
        httpx_mock.add_response(content=wifi_guest_access_set.SerializeToString())
        assert device_api.set_wifi_guest_access(True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_get_wifi_neighbor_access_points(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting neighboring wifi access points asynchronously."""
        wifi_neighbor_accesspoints_get = WifiNeighborAPsGet()
        httpx_mock.add_response(content=wifi_neighbor_accesspoints_get.SerializeToString())
        wifi_neighbor_access_points = await device_api.async_get_wifi_neighbor_access_points()
        assert wifi_neighbor_access_points == MessageToDict(
            wifi_neighbor_accesspoints_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_get_wifi_neighbor_access_points(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test getting neighboring wifi access points synchronously."""
        wifi_neighbor_accesspoints_get = WifiNeighborAPsGet()
        httpx_mock.add_response(content=wifi_neighbor_accesspoints_get.SerializeToString())
        wifi_neighbor_access_points = device_api.get_wifi_neighbor_access_points()
        assert wifi_neighbor_access_points == MessageToDict(
            wifi_neighbor_accesspoints_get, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", ["wifi1"])
    async def test_async_start_wps(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test starting WPS asynchronously."""
        wps = WifiWpsPbcStart()
        httpx_mock.add_response(content=wps.SerializeToString())
        assert await device_api.async_start_wps()

    @pytest.mark.parametrize("feature", ["wifi1"])
    def test_start_wps(self, device_api: DeviceApi, httpx_mock: HTTPXMock):
        """Test starting WPS synchronously."""
        wps = WifiWpsPbcStart()
        httpx_mock.add_response(content=wps.SerializeToString())
        assert device_api.start_wps()
