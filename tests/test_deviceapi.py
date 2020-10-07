from unittest.mock import patch

import pytest
from google.protobuf.json_format import MessageToDict
from httpx import AsyncClient, Client, Response

try:
    from mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from devolo_plc_api.device_api.deviceapi import DeviceApi
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsGet, LedSettingsSetResponse
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_wifinetwork_pb2 import (
    WifiConnectedStationsGet, WifiGuestAccessGet, WifiGuestAccessSetResponse, WifiNeighborAPsGet, WifiRepeatedAPsGet,
    WifiWpsPbcStart)
from devolo_plc_api.exceptions.feature import FeatureNotSupported
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_updatefirmware_pb2 import UpdateFirmwareCheck, UpdateFirmwareStart


class TestDeviceApi:

    def test_unsupported_feature(self, request):
        with pytest.raises(FeatureNotSupported):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "[]",
                                   "password")
            device_api.get_led_setting()

    @pytest.mark.asyncio
    async def test_async_get_led_setting(self, request):
        led_setting_get = LedSettingsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=led_setting_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "led",
                                   "password")
            led_setting = await device_api.async_get_led_setting()

        assert led_setting == MessageToDict(led_setting_get,
                                            including_default_value_fields=True,
                                            preserving_proto_field_name=True)

    def test_get_led_setting(self, request):
        led_setting_get = LedSettingsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=led_setting_get.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "led",
                                   "password")
            led_setting = device_api.get_led_setting()

        assert led_setting == MessageToDict(led_setting_get,
                                            including_default_value_fields=True,
                                            preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_set_led_setting(self, request):
        led_setting_set = LedSettingsSetResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=led_setting_set.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "led",
                                   "password")

            assert await device_api.async_set_led_setting(True)

    def test_set_led_setting(self, request):
        led_setting_set = LedSettingsSetResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._post", return_value=Response), \
             patch("httpx.Response.read", return_value=led_setting_set.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "led",
                                   "password")

            assert device_api.set_led_setting(True)

    @pytest.mark.asyncio
    async def test_async_check_firmware_available(self, request):
        firmware_available = UpdateFirmwareCheck()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=firmware_available.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "update",
                                   "password")
            firmware = await device_api.async_check_firmware_available()

            assert firmware == MessageToDict(firmware_available,
                                             including_default_value_fields=True,
                                             preserving_proto_field_name=True)

    def test_check_firmware_available(self, request):
        firmware_available = UpdateFirmwareCheck()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=firmware_available.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "update",
                                   "password")
            firmware = device_api.check_firmware_available()

            assert firmware == MessageToDict(firmware_available,
                                             including_default_value_fields=True,
                                             preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_start_firmware_update(self, request):
        firmware_update = UpdateFirmwareStart()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=firmware_update.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "update",
                                   "password")

            assert await device_api.async_start_firmware_update()

    def test_start_firmware_update(self, request):
        firmware_update = UpdateFirmwareStart()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=firmware_update.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "update",
                                   "password")

            assert device_api.start_firmware_update()

    @pytest.mark.asyncio
    async def test_async_get_wifi_connected_station(self, request):
        wifi_connected_stations_get = WifiConnectedStationsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_connected_stations_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            connected_stations = await device_api.async_get_wifi_connected_station()

        assert connected_stations == MessageToDict(wifi_connected_stations_get,
                                                   including_default_value_fields=True,
                                                   preserving_proto_field_name=True)

    def test_get_wifi_connected_station(self, request):
        wifi_connected_stations_get = WifiConnectedStationsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=wifi_connected_stations_get.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            connected_stations = device_api.get_wifi_connected_station()

        assert connected_stations == MessageToDict(wifi_connected_stations_get,
                                                   including_default_value_fields=True,
                                                   preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_get_wifi_guest_access(self, request):
        wifi_guest_access_get = WifiGuestAccessGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_guest_access_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_guest_access = await device_api.async_get_wifi_guest_access()

        assert wifi_guest_access == MessageToDict(wifi_guest_access_get,
                                                  including_default_value_fields=True,
                                                  preserving_proto_field_name=True)

    def test_get_wifi_guest_access(self, request):
        wifi_guest_access_get = WifiGuestAccessGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=wifi_guest_access_get.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_guest_access = device_api.get_wifi_guest_access()

        assert wifi_guest_access == MessageToDict(wifi_guest_access_get,
                                                  including_default_value_fields=True,
                                                  preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_set_wifi_guest_access(self, request):
        wifi_guest_access_set = WifiGuestAccessSetResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_guest_access_set.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")

            assert await device_api.async_set_wifi_guest_access(True)

    def test_set_wifi_guest_access(self, request):
        wifi_guest_access_set = WifiGuestAccessSetResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._post", return_value=Response), \
             patch("httpx.Response.read", return_value=wifi_guest_access_set.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")

            assert device_api.set_wifi_guest_access(True)

    @pytest.mark.asyncio
    async def test_async_get_wifi_neighbor_access_points(self, request):
        wifi_neighbor_accesspoints_get = WifiNeighborAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_neighbor_accesspoints_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_neighbor_access_points = await device_api.async_get_wifi_neighbor_access_points()

        assert wifi_neighbor_access_points == MessageToDict(wifi_neighbor_accesspoints_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    def test_get_wifi_neighbor_access_points(self, request):
        wifi_neighbor_access_points_get = WifiNeighborAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=wifi_neighbor_access_points_get.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_neighbor_access_points = device_api.get_wifi_neighbor_access_points()

        assert wifi_neighbor_access_points == MessageToDict(wifi_neighbor_access_points_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_get_wifi_repeated_access_points(self, request):
        wifi_repeated_accesspoints_get = WifiRepeatedAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=wifi_repeated_accesspoints_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_repeated_access_points = await device_api.async_get_wifi_repeated_access_points()

        assert wifi_repeated_access_points == MessageToDict(wifi_repeated_accesspoints_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    def test_get_wifi_repeated_access_points(self, request):
        wifi_repeated_access_points_get = WifiRepeatedAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=wifi_repeated_access_points_get.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_repeated_access_points = device_api.get_wifi_repeated_access_points()

        assert wifi_repeated_access_points == MessageToDict(wifi_repeated_access_points_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_start_wps(self, request):
        wps = WifiWpsPbcStart()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=wps.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")

            assert await device_api.async_start_wps()

    def test_start_wps(self, request):
        wps = WifiWpsPbcStart()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=wps.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")

            assert device_api.start_wps()
