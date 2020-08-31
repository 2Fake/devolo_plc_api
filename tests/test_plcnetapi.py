from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from google.protobuf.json_format import MessageToDict
from httpx import AsyncClient, Client, Response

from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi
from devolo_plc_api.plcnet_api.devolo_idl_proto_plcnetapi_getnetworkoverview_pb2 import GetNetworkOverview


class TestDeviceApi:

    @pytest.mark.asyncio
    async def test_async_get_network_overview(self, request):
        network_overview = GetNetworkOverview()

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=network_overview.SerializeToString())):
            plcnet_api = PlcNetApi(request.cls.ip,
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
                                   Client(),
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                                   request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])
            overview = plcnet_api.get_network_overview()

        assert overview == MessageToDict(network_overview,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True)
