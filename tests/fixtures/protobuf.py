import logging

import pytest

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from ..stubs.protobuf import Protobuf


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
    mocker.patch("httpx.AsyncClient.get", new=AsyncMock())
    mocker.patch("httpx.Client.get", return_value=None)


@pytest.fixture()
def mock_post(mocker):
    mocker.patch("httpx.AsyncClient.post", new=AsyncMock())
    mocker.patch("httpx.Client.post", return_value=None)


@pytest.fixture()
def mock_wrong_password(mocker):
    mocker.patch("httpx.AsyncClient.get", side_effect=TypeError())
    mocker.patch("httpx.Client.get", side_effect=TypeError())
    mocker.patch("httpx.AsyncClient.post", side_effect=TypeError())
    mocker.patch("httpx.Client.post", side_effect=TypeError())
