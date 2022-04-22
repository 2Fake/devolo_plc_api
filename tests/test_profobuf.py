from http import HTTPStatus

import pytest
from httpx import ConnectTimeout, HTTPStatusError
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture

from devolo_plc_api.clients import protobuf
from devolo_plc_api.device_api.ledsettings_pb2 import LedSettingsSetResponse
from devolo_plc_api.exceptions.device import DevicePasswordProtected, DeviceUnavailable
from devolo_plc_api.plcnet_api import SERVICE_TYPE

from .stubs.protobuf import StubProtobuf


class TestProtobuf:
    def test_attribute_error(self, mock_protobuf: StubProtobuf):
        with pytest.raises(AttributeError):
            mock_protobuf.test()

    def test_url(self, request: pytest.FixtureRequest, mock_protobuf: StubProtobuf):
        ip = request.cls.ip
        path = request.cls.device_info[SERVICE_TYPE]["properties"]["Path"]
        version = request.cls.device_info[SERVICE_TYPE]["properties"]["Version"]
        assert mock_protobuf.url == f"http://{ip}:14791/{path}/{version}/"

    @pytest.mark.asyncio
    async def test__async_get(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response()
        await mock_protobuf._async_get("LedSettingsGet")
        assert httpx_mock.get_request()

    @pytest.mark.asyncio
    async def test__async_get_wrong_password(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_get("LedSettingsGet")

    @pytest.mark.asyncio
    async def test__async_get_device_unavailable(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_exception(ConnectTimeout("ConnectTimeout"))
        with pytest.raises(DeviceUnavailable):
            await mock_protobuf._async_get("LedSettingsGet")

    @pytest.mark.asyncio
    async def test__async_get_unknown_error(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response(status_code=HTTPStatus.SERVICE_UNAVAILABLE)
        with pytest.raises(HTTPStatusError):
            await mock_protobuf._async_get("LedSettingsGet")

    def test__message_to_dict(self, mocker: MockerFixture, mock_protobuf: StubProtobuf):
        spy = mocker.spy(protobuf, "MessageToDict")
        mock_protobuf._message_to_dict(LedSettingsSetResponse())
        spy.assert_called_once()

    @pytest.mark.asyncio
    async def test__async_post(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response()
        await mock_protobuf._async_post("LedSettingsGet", b"")
        assert httpx_mock.get_request()

    @pytest.mark.asyncio
    async def test__async_post_wrong_password(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_post("LedSettingsGet", b"")

    @pytest.mark.asyncio
    async def test__async_post_device_unavailable(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_exception(ConnectTimeout("ConnectTimeout"))
        with pytest.raises(DeviceUnavailable):
            await mock_protobuf._async_post("LedSettingsGet", b"")

    @pytest.mark.asyncio
    async def test__async_post_unknown_error(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response(status_code=HTTPStatus.SERVICE_UNAVAILABLE)
        with pytest.raises(HTTPStatusError):
            await mock_protobuf._async_post("LedSettingsGet", b"")

    @pytest.mark.asyncio
    async def test__async_wrong_password_type(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_get("LedSettingsGet", b"")

        assert httpx_mock.get_requests()
        assert mock_protobuf.password == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

        httpx_mock.add_response(status_code=HTTPStatus.UNAUTHORIZED)
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_post("LedSettingsSet", b"")

        assert httpx_mock.get_requests()
        assert mock_protobuf.password == "113459eb7bb31bddee85ade5230d6ad5d8b2fb52879e00a84ff6ae1067a210d3"
