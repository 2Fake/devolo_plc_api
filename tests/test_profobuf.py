import google.protobuf.json_format
import httpx
import pytest

from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsSetResponse
from devolo_plc_api.exceptions.device import DevicePasswordProtected


class TestProtobuf:
    def test_url(self, request, mock_protobuf):
        ip = request.cls.ip
        path = request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path']
        version = request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version']

        assert mock_protobuf.url == f"http://{ip}:14791/{path}/{version}/"

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_get")
    async def test__async_get(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.AsyncClient()
        spy = mocker.spy(httpx.AsyncClient, "get")
        await mock_protobuf._async_get("LedSettingsGet")

        spy.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_wrong_password")
    async def test__async_get_wrong_password(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.AsyncClient()
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_get("LedSettingsGet")

    @pytest.mark.usefixtures("mock_get")
    def test__get(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.Client()
        spy = mocker.spy(httpx.Client, "get")
        mock_protobuf._get("LedSettingsGet")

        spy.assert_called_once()

    @pytest.mark.usefixtures("mock_wrong_password")
    def test__get_wrong_password(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.Client()
        with pytest.raises(DevicePasswordProtected):
            mock_protobuf._get("LedSettingsGet")

    def test__message_to_dict(self, mocker, mock_protobuf):
        spy = mocker.spy(google.protobuf.json_format._Printer, "_MessageToJsonObject")
        mock_protobuf._message_to_dict(LedSettingsSetResponse())

        spy.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_post")
    async def test__async_post(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.AsyncClient()
        spy = mocker.spy(httpx.AsyncClient, "post")
        await mock_protobuf._async_post("LedSettingsGet", "")

        spy.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_wrong_password")
    async def test__async_post_wrong_password(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.AsyncClient()
        with pytest.raises(DevicePasswordProtected):
            await mock_protobuf._async_post("LedSettingsGet", "")

    @pytest.mark.usefixtures("mock_post")
    def test__post(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.Client()
        spy = mocker.spy(httpx.Client, "post")
        mock_protobuf._post("LedSettingsGet", "")

        spy.assert_called_once()

    @pytest.mark.usefixtures("mock_wrong_password")
    def test__post_wrong_password(self, mocker, mock_protobuf):
        mock_protobuf._session = httpx.Client()
        with pytest.raises(DevicePasswordProtected):
            mock_protobuf._post("LedSettingsGet", "")
