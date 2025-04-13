"""Test communicating with a the plcnet API."""

import sys
from http import HTTPStatus
from unittest.mock import patch

import pytest
from httpx import ConnectTimeout
from pytest_httpx import HTTPXMock

from devolo_plc_api import Device
from devolo_plc_api.exceptions import DevicePasswordProtected, DeviceUnavailable
from devolo_plc_api.plcnet_api import LogicalNetwork, PlcNetApi
from devolo_plc_api.plcnet_api.getnetworkoverview_pb2 import GetNetworkOverview
from devolo_plc_api.plcnet_api.identifydevice_pb2 import IdentifyDeviceResponse
from devolo_plc_api.plcnet_api.pairdevice_pb2 import PairDeviceStart
from devolo_plc_api.plcnet_api.setuserdevicename_pb2 import SetUserDeviceNameResponse

from . import DeviceType


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Tests with httpx_mock need at least Python 3.9")
class TestPlcApi:
    """Test devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi class."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("block_communication", "service_browser")
    @pytest.mark.httpx_mock(can_send_already_matched_responses=True)
    async def test_wrong_password_type(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test using different password hash if original password failed."""
        await mock_device.async_connect()
        assert mock_device.plcnet
        mock_device.password = "password"

        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_device.plcnet.async_set_user_device_name("Test")
            assert mock_device.plcnet.password == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_device.plcnet.async_set_user_device_name("Test")
            assert mock_device.plcnet.password == "113459eb7bb31bddee85ade5230d6ad5d8b2fb52879e00a84ff6ae1067a210d3"

        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test_async_get_network_overview(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock, network: LogicalNetwork):
        """Test getting the network overview asynchronously."""
        network_overview = GetNetworkOverview(network=network)
        httpx_mock.add_response(content=network_overview.SerializeToString())
        overview = await plcnet_api.async_get_network_overview()
        assert overview == network

    def test_get_network_overview(self, plcnet_api: PlcNetApi, httpx_mock: HTTPXMock, network: LogicalNetwork):
        """Test getting the network overview synchronously."""
        network_overview = GetNetworkOverview(network=network)
        httpx_mock.add_response(content=network_overview.SerializeToString())
        overview = plcnet_api.get_network_overview()
        assert overview == network

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

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("block_communication", "service_browser")
    async def test_device_unavailable(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test device being unavailable."""
        await mock_device.async_connect()
        assert mock_device.plcnet
        httpx_mock.add_exception(ConnectTimeout(""), is_reusable=True)
        with pytest.raises(DeviceUnavailable), patch("asyncio.sleep"):
            await mock_device.plcnet.async_get_network_overview()
        await mock_device.async_disconnect()
        assert len(httpx_mock.get_requests()) == 3

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("block_communication", "service_browser")
    async def test_attribute_error(self, mock_device: Device):
        """Test raising on calling not existing method."""
        await mock_device.async_connect()
        assert mock_device.plcnet
        with pytest.raises(AttributeError):
            mock_device.plcnet.test()  # type: ignore[union-attr]
