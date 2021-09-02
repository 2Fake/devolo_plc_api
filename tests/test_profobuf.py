import google.protobuf.json_format
import httpx
import pytest

from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsSetResponse
from devolo_plc_api.exceptions.device import DevicePasswordProtected, DeviceUnavailable


class TestProtobuf:

    def test_attribute_error(self, mock_protobuf):
        with pytest.raises(AttributeError):
            mock_protobuf.test()

    def test_url(self, request, mock_protobuf):
        ip = request.cls.ip
        path = request.cls.device_info["_dvl-plcnetapi._tcp.local."]["properties"]["Path"]
        version = request.cls.device_info["_dvl-plcnetapi._tcp.local."]["properties"]["Version"]
        assert mock_protobuf.url == f"http://{ip}:14791/{path}/{version}/"

    @pytest.mark.asyncio
    async def test__async_get(self, httpx_mock, mocker, mock_protobuf):
        httpx_mock.add_response()
        spy = mocker.spy(httpx.AsyncClient, "get")
        await mock_protobuf._async_get("LedSettingsGet")
        spy.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_wrong_password")
    async def test__async_get_wrong_password(self, mock_protobuf):
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_get("LedSettingsGet")

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_unavailable")
    async def test__async_get_device_unavailable(self, mock_protobuf):
        with pytest.raises(DeviceUnavailable):
            await mock_protobuf._async_get("LedSettingsGet")

    def test__message_to_dict(self, mocker, mock_protobuf):
        spy = mocker.spy(google.protobuf.json_format._Printer, "_MessageToJsonObject")
        mock_protobuf._message_to_dict(LedSettingsSetResponse())
        spy.assert_called_once()

    @pytest.mark.asyncio
    async def test__async_post(self, httpx_mock, mocker, mock_protobuf):
        httpx_mock.add_response()
        spy = mocker.spy(httpx.AsyncClient, "post")
        await mock_protobuf._async_post("LedSettingsGet", "")
        spy.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_wrong_password")
    async def test__async_post_wrong_password(self, mock_protobuf):
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_post("LedSettingsGet", "")

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_unavailable")
    async def test__async_post_device_unavailable(self, mock_protobuf):
        with pytest.raises(DeviceUnavailable):
            await mock_protobuf._async_post("LedSettingsGet", "")
