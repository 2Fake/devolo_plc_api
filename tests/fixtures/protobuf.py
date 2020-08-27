import logging

import pytest

from devolo_plc_api.clients.protobuf import Protobuf

from ..mocks.mock_httpx import AsyncClient, Client


@pytest.fixture()
def mock_protobuf(request):
    protobuf = Protobuf()
    protobuf._logger = logging.getLogger("ProtobufMock")
    protobuf._ip = request.cls.ip
    protobuf._port = 14791
    protobuf._path = request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path']
    protobuf._version = request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version']
    protobuf._user = "user"
    protobuf._password = "password"
    return protobuf


@pytest.fixture()
def mock_get(mocker):
    mocker.patch("httpx.AsyncClient.get", AsyncClient.get)
    mocker.patch("httpx.Client.get", Client.get)


@pytest.fixture()
def mock_post(mocker):
    mocker.patch("httpx.AsyncClient.post", AsyncClient.post)
    mocker.patch("httpx.Client.post", Client.post)


@pytest.fixture()
def mock_wrong_password(mocker):
    mocker.patch("httpx.AsyncClient.get", AsyncClient.wrong_password)
    mocker.patch("httpx.Client.get", Client.wrong_password)
    mocker.patch("httpx.AsyncClient.post", AsyncClient.wrong_password)
    mocker.patch("httpx.Client.post", Client.wrong_password)
