"""Test API independent communication."""
from http import HTTPStatus

import pytest
from httpx import ConnectTimeout, HTTPStatusError
from pytest_httpx import HTTPXMock

from devolo_plc_api.device import Device
from devolo_plc_api.exceptions.device import DevicePasswordProtected, DeviceUnavailable
from devolo_plc_api.plcnet_api import SERVICE_TYPE

from . import TestData
from .stubs.protobuf import StubProtobuf


class TestProtobuf:
    """Test devolo_plc_api.clients.protobuf.Protobuf class."""

    def test_attribute_error(self, mock_protobuf: StubProtobuf):
        """Test raising on calling not existing method."""
        with pytest.raises(AttributeError):
            mock_protobuf.test()

    def test_url(self, test_data: TestData, mock_protobuf: StubProtobuf):
        """Test generating the url to use for device communication."""
        ip = test_data.ip
        path = test_data.device_info[SERVICE_TYPE]["properties"]["Path"]
        version = test_data.device_info[SERVICE_TYPE]["properties"]["Version"]
        assert mock_protobuf.url == f"http://{ip}:14791/{path}/{version}/"

    @pytest.mark.asyncio
    async def test__async_get_wrong_password(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test raising on using a wrong password."""
        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        await mock_device.async_connect()
        assert mock_device.device
        with pytest.raises(DevicePasswordProtected):
            await mock_device.device.async_get_wifi_connected_station()
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test__async_get_device_unavailable(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test raising on connection timeout."""
        httpx_mock.add_exception(ConnectTimeout("ConnectTimeout"))
        await mock_device.async_connect()
        assert mock_device.device
        with pytest.raises(DeviceUnavailable):
            await mock_device.device.async_get_wifi_connected_station()
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test__async_get_unknown_error(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test re-raising unexpected HTTP errors."""
        httpx_mock.add_response(status_code=HTTPStatus.SERVICE_UNAVAILABLE)
        await mock_device.async_connect()
        assert mock_device.device
        with pytest.raises(HTTPStatusError):
            await mock_device.device.async_get_wifi_connected_station()
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test__async_post_wrong_password(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test raising on using a wrong password."""
        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        await mock_device.async_connect()
        assert mock_device.device
        with pytest.raises(DevicePasswordProtected):
            await mock_device.device.async_set_wifi_guest_access(True)
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test__async_post_device_unavailable(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test raising on connection timeout."""
        httpx_mock.add_exception(ConnectTimeout("ConnectTimeout"))
        await mock_device.async_connect()
        assert mock_device.device
        with pytest.raises(DeviceUnavailable):
            await mock_device.device.async_set_wifi_guest_access(True)
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test__async_post_unknown_error(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test re-raising unexpected HTTP errors."""
        httpx_mock.add_response(status_code=HTTPStatus.SERVICE_UNAVAILABLE)
        await mock_device.async_connect()
        assert mock_device.device
        with pytest.raises(HTTPStatusError):
            await mock_device.device.async_get_wifi_connected_station()
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test__async_wrong_password_type(self, httpx_mock: HTTPXMock, mock_device: Device):
        """Test using different password hash if original password failed."""
        await mock_device.async_connect()
        assert mock_device.device
        mock_device.password = "password"

        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_device.device.async_get_wifi_connected_station()
            assert mock_device.device.password == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_device.device.async_get_wifi_connected_station()
            assert mock_device.device.password == "113459eb7bb31bddee85ade5230d6ad5d8b2fb52879e00a84ff6ae1067a210d3"

        await mock_device.async_disconnect()
