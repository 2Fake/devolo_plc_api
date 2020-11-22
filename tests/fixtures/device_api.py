from unittest.mock import patch

import pytest
from devolo_plc_api.device_api.deviceapi import DeviceApi
from httpx import AsyncClient, Client, Response

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock


@pytest.fixture()
def device_api_async(request, feature):
    with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
         patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)):
        yield DeviceApi(request.cls.ip,
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                        AsyncClient(),
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                        feature,
                        "password")


@pytest.fixture()
def device_api_sync(request, feature):
    with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
         patch("devolo_plc_api.clients.protobuf.Protobuf._post", return_value=Response):
        yield DeviceApi(request.cls.ip,
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                        Client(),
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                        feature,
                        "password")


@pytest.fixture()
def mock_device_api(mocker):
    mocker.patch("devolo_plc_api.device_api.deviceapi.DeviceApi.__init__", return_value=None)
