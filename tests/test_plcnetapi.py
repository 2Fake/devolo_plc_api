from unittest.mock import patch

import pytest
from google.protobuf.json_format import MessageToDict
from httpx import AsyncClient, Client, Response

try:
    from mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from devolo_plc_api.plcnet_api.devolo_idl_proto_plcnetapi_getnetworkoverview_pb2 import GetNetworkOverview
from devolo_plc_api.plcnet_api.devolo_idl_proto_plcnetapi_identifydevice_pb2 import IdentifyDeviceResponse
from devolo_plc_api.plcnet_api.devolo_idl_proto_plcnetapi_setuserdevicename_pb2 import SetUserDeviceNameResponse
from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi


class TestDeviceApi:

    @pytest.mark.asyncio
    async def test_async_get_network_overview(self, request):
        network_overview = GetNetworkOverview()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=network_overview.SerializeToString())):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])
            overview = await plcnet_api.async_get_network_overview()

        assert overview == MessageToDict(network_overview,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True)

    def test_get_network_overview(self, request):
        network_overview = GetNetworkOverview()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
             patch("httpx.Response.read", return_value=network_overview.SerializeToString()):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])
            overview = plcnet_api.get_network_overview()

        assert overview == MessageToDict(network_overview,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_identify_device_start(self, request):
        identify_device = IdentifyDeviceResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=identify_device.SerializeToString())):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])

            assert await plcnet_api.async_identify_device_start()

    def test_identify_device_start(self, request):
        identify_device = IdentifyDeviceResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._post", return_value=Response), \
             patch("httpx.Response.read", return_value=identify_device.SerializeToString()):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])

            assert plcnet_api.identify_device_start()

    @pytest.mark.asyncio
    async def test_async_identify_device_stop(self, request):
        identify_device = IdentifyDeviceResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=identify_device.SerializeToString())):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])

            assert await plcnet_api.async_identify_device_stop()

    def test_identify_device_stop(self, request):
        identify_device = IdentifyDeviceResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._post", return_value=Response), \
             patch("httpx.Response.read", return_value=identify_device.SerializeToString()):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])

            assert plcnet_api.identify_device_stop()

    @pytest.mark.asyncio
    async def test_async_set_user_device_name(self, request):
        user_device_name_set = SetUserDeviceNameResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)), \
             patch("httpx.Response.aread", new=AsyncMock(return_value=user_device_name_set.SerializeToString())):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])

            assert await plcnet_api.async_set_user_device_name("Test")

    def test_set_user_device_name(self, request):
        user_device_name_set = SetUserDeviceNameResponse()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._post", return_value=Response), \
             patch("httpx.Response.read", return_value=user_device_name_set.SerializeToString()):
            plcnet_api = PlcNetApi(request.cls.ip,
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])

            assert plcnet_api.set_user_device_name("Test")
