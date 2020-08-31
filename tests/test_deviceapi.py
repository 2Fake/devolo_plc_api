from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from google.protobuf.json_format import MessageToDict
from httpx import AsyncClient, Client, Response

from devolo_plc_api.device_api.deviceapi import DeviceApi
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsGet
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_wifinetwork_pb2 import (
    WifiConnectedStationsGet, WifiGuestAccessGet, WifiNeighborAPsGet, WifiRepeatedAPsGet)
from devolo_plc_api.exceptions.feature import FeatureNotSupported


class TestDeviceApi:

    def test_unsupported_feature(self, request):
        with pytest.raises(FeatureNotSupported):
            device_api = DeviceApi(request.cls.ip,
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "",
                                   "password")
            device_api.get_led_setting()

    @pytest.mark.asyncio
    async def test_async_get_led_setting(self, request):
        led_setting_get = LedSettingsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=led_setting_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
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
    async def test_async_get_wifi_connected_station(self, request):
        wifi_connected_stations_get = WifiConnectedStationsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=wifi_connected_stations_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
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

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=wifi_guest_access_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
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
    async def test_async_get_wifi_neighbor_access_points(self, request):
        wifi_neighbor_access_points_get = WifiNeighborAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=wifi_neighbor_access_points_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_neighbor_access_points = await device_api.async_get_wifi_neighbor_access_points()

        assert wifi_neighbor_access_points == MessageToDict(wifi_neighbor_access_points_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    def test_get_wifi_neighbor_access_points(self, request):
        wifi_neighbor_access_points_get = WifiNeighborAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=wifi_neighbor_access_points_get.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
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
        wifi_repeated_access_points_get = WifiRepeatedAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=wifi_repeated_access_points_get.SerializeToString())):
            device_api = DeviceApi(request.cls.ip,
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_repeated_access_points = await device_api.async_get_wifi_repeated_access_points()

        assert wifi_repeated_access_points == MessageToDict(wifi_repeated_access_points_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)

    def test_get_wifi_repeated_access_points(self, request):
        wifi_repeated_access_points_get = WifiRepeatedAPsGet()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=wifi_repeated_access_points_get.SerializeToString()):
            device_api = DeviceApi(request.cls.ip,
                                   Client(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "wifi1",
                                   "password")
            wifi_repeated_access_points = device_api.get_wifi_repeated_access_points()

        assert wifi_repeated_access_points == MessageToDict(wifi_repeated_access_points_get,
                                                            including_default_value_fields=True,
                                                            preserving_proto_field_name=True)
