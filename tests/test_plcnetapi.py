"""Test communicating with a the plcnet API."""
import pytest
from google.protobuf.json_format import MessageToDict
from pytest_httpx import HTTPXMock

from devolo_plc_api.plcnet_api.getnetworkoverview_pb2 import GetNetworkOverview
from devolo_plc_api.plcnet_api.identifydevice_pb2 import IdentifyDeviceResponse
from devolo_plc_api.plcnet_api.pairdevice_pb2 import PairDeviceStart
from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi
from devolo_plc_api.plcnet_api.setuserdevicename_pb2 import SetUserDeviceNameResponse


class TestDeviceApi:
    """Test devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi class."""

    @pytest.mark.asyncio
    async def test_async_get_network_overview(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test getting the network overview asynchronously."""
        network_overview = GetNetworkOverview()
        httpx_mock.add_response(content=network_overview.SerializeToString())
        overview = await plcnet_api.async_get_network_overview()
        assert overview == MessageToDict(
            network_overview, including_default_value_fields=True, preserving_proto_field_name=True
        )

    def test_get_network_overview(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test getting the network overview synchronously."""
        network_overview = GetNetworkOverview()
        httpx_mock.add_response(content=network_overview.SerializeToString())
        overview = plcnet_api.get_network_overview()
        assert overview == MessageToDict(
            network_overview, including_default_value_fields=True, preserving_proto_field_name=True
        )

    @pytest.mark.asyncio
    async def test_async_identify_device_start(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test starting identifying a device asynchronously."""
        identify_device = IdentifyDeviceResponse()
        httpx_mock.add_response(content=identify_device.SerializeToString())
        assert await plcnet_api.async_identify_device_start()

    def test_identify_device_start(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test starting identifying a device synchronously."""
        identify_device = IdentifyDeviceResponse()
        httpx_mock.add_response(content=identify_device.SerializeToString())
        assert plcnet_api.identify_device_start()

    @pytest.mark.asyncio
    async def test_async_identify_device_stop(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test stopping identifying a device asynchronously."""
        identify_device = IdentifyDeviceResponse()
        httpx_mock.add_response(content=identify_device.SerializeToString())
        assert await plcnet_api.async_identify_device_stop()

    def test_identify_device_stop(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test stopping identifying a device synchronously."""
        identify_device = IdentifyDeviceResponse()
        httpx_mock.add_response(content=identify_device.SerializeToString())
        assert plcnet_api.identify_device_stop()

    @pytest.mark.asyncio
    async def test_async_pair_device(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test pairing a device asynchronously."""
        pair_device = PairDeviceStart()
        httpx_mock.add_response(content=pair_device.SerializeToString())
        assert await plcnet_api.async_pair_device()

    def test_pair_device(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test pairing a device synchronously."""
        pair_device = PairDeviceStart()
        httpx_mock.add_response(content=pair_device.SerializeToString())
        assert plcnet_api.pair_device()

    @pytest.mark.asyncio
    async def test_async_set_user_device_name(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test setting a device name asynchronously."""
        user_device_name_set = SetUserDeviceNameResponse()
        httpx_mock.add_response(content=user_device_name_set.SerializeToString())
        assert await plcnet_api.async_set_user_device_name("Test")

    def test_set_user_device_name(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock):
        """Test setting a device name synchronously."""
        user_device_name_set = SetUserDeviceNameResponse()
        httpx_mock.add_response(content=user_device_name_set.SerializeToString())
        assert plcnet_api.set_user_device_name("Test")
