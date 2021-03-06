from unittest.mock import patch

import pytest
from google.protobuf.json_format import MessageToDict

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from devolo_plc_api.plcnet_api.devolo_idl_proto_plcnetapi_getnetworkoverview_pb2 import GetNetworkOverview
from devolo_plc_api.plcnet_api.devolo_idl_proto_plcnetapi_identifydevice_pb2 import IdentifyDeviceResponse
from devolo_plc_api.plcnet_api.devolo_idl_proto_plcnetapi_setuserdevicename_pb2 import SetUserDeviceNameResponse


class TestDeviceApi:

    @pytest.mark.asyncio
    async def test_async_get_network_overview(self, plcnet_api):
        network_overview = GetNetworkOverview()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=network_overview.SerializeToString())):
            overview = await plcnet_api.async_get_network_overview()
            assert overview == MessageToDict(network_overview,
                                             including_default_value_fields=True,
                                             preserving_proto_field_name=True)

    def test_get_network_overview(self, plcnet_api):
        network_overview = GetNetworkOverview()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=network_overview.SerializeToString())):
            overview = plcnet_api.get_network_overview()
            assert overview == MessageToDict(network_overview,
                                             including_default_value_fields=True,
                                             preserving_proto_field_name=True)

    @pytest.mark.asyncio
    async def test_async_identify_device_start(self, plcnet_api):
        identify_device = IdentifyDeviceResponse()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=identify_device.SerializeToString())):
            assert await plcnet_api.async_identify_device_start()

    def test_identify_device_start(self, plcnet_api):
        identify_device = IdentifyDeviceResponse()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=identify_device.SerializeToString())):
            assert plcnet_api.identify_device_start()

    @pytest.mark.asyncio
    async def test_async_identify_device_stop(self, plcnet_api):
        identify_device = IdentifyDeviceResponse()

        with patch("httpx.Response.aread", new=AsyncMock(return_value=identify_device.SerializeToString())):
            assert await plcnet_api.async_identify_device_stop()

    def test_identify_device_stop(self, plcnet_api):
        identify_device = IdentifyDeviceResponse()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=identify_device.SerializeToString())):
            assert plcnet_api.identify_device_stop()

    @pytest.mark.asyncio
    async def test_async_set_user_device_name(self, plcnet_api):
        user_device_name_set = SetUserDeviceNameResponse()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=user_device_name_set.SerializeToString())):
            assert await plcnet_api.async_set_user_device_name("Test")

    def test_set_user_device_name(self, plcnet_api):
        user_device_name_set = SetUserDeviceNameResponse()
        with patch("httpx.Response.aread", new=AsyncMock(return_value=user_device_name_set.SerializeToString())):
            assert plcnet_api.set_user_device_name("Test")
