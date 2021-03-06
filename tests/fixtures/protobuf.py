import pytest
from httpx import ConnectTimeout

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from ..stubs.protobuf import StubProtobuf


@pytest.fixture()
def mock_protobuf():
    return StubProtobuf()


@pytest.fixture()
def mock_get(mocker):
    mocker.patch("httpx.AsyncClient.get", new=AsyncMock())


@pytest.fixture()
def mock_post(mocker):
    mocker.patch("httpx.AsyncClient.post", new=AsyncMock())


@pytest.fixture()
def mock_device_unavailable(mocker):
    mocker.patch("httpx.AsyncClient.get", side_effect=ConnectTimeout(message="", request=""))
    mocker.patch("httpx.AsyncClient.post", side_effect=ConnectTimeout(message="", request=""))


@pytest.fixture()
def mock_wrong_password(mocker):
    mocker.patch("httpx.AsyncClient.get", side_effect=TypeError())
    mocker.patch("httpx.AsyncClient.post", side_effect=TypeError())
