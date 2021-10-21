import pytest
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture

from devolo_plc_api.clients import protobuf
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsSetResponse
from devolo_plc_api.exceptions.device import DevicePasswordProtected, DeviceUnavailable

from .stubs.protobuf import StubProtobuf


class TestProtobuf:

    def test_attribute_error(self, mock_protobuf: StubProtobuf):
        with pytest.raises(AttributeError):
            mock_protobuf.test()

    def test_url(self, request: pytest.FixtureRequest, mock_protobuf: StubProtobuf):
        ip = request.cls.ip
        path = request.cls.device_info["_dvl-plcnetapi._tcp.local."]["properties"]["Path"]
        version = request.cls.device_info["_dvl-plcnetapi._tcp.local."]["properties"]["Version"]
        assert mock_protobuf.url == f"http://{ip}:14791/{path}/{version}/"

    @pytest.mark.asyncio
    async def test__async_get(self, httpx_mock: HTTPXMock, mock_protobuf: StubProtobuf):
        httpx_mock.add_response()
        await mock_protobuf._async_get("LedSettingsGet")
        assert httpx_mock.get_request()

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_wrong_password")
    async def test__async_get_wrong_password(self, mock_protobuf: StubProtobuf):
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_get("LedSettingsGet")

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_unavailable")
    async def test__async_get_device_unavailable(self, mock_protobuf: StubProtobuf):
        with pytest.raises(DeviceUnavailable):
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
    @pytest.mark.usefixtures("mock_wrong_password")
    async def test__async_post_wrong_password(self, mock_protobuf: StubProtobuf):
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_post("LedSettingsGet", b"")

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_unavailable")
    async def test__async_post_device_unavailable(self, mock_protobuf: StubProtobuf):
        with pytest.raises(DeviceUnavailable):
            await mock_protobuf._async_post("LedSettingsGet", b"")
