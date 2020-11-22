from unittest.mock import patch

import pytest
from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi
from httpx import AsyncClient, Client, Response

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock


@pytest.fixture()
def plcnet_api_async(request):
    with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
         patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)):
        yield PlcNetApi(request.cls.ip,
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                        AsyncClient(),
                        request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                        request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                        request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])


@pytest.fixture()
def plcnet_api_sync(request):
    with patch("devolo_plc_api.clients.protobuf.Protobuf._get", return_value=Response), \
         patch("devolo_plc_api.clients.protobuf.Protobuf._post", return_value=Response):
        yield PlcNetApi(request.cls.ip,
                        request.cls.device_info['_dvl-deviceapi._tcp.local.']['Port'],
                        Client(),
                        request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Path'],
                        request.cls.device_info['_dvl-plcnetapi._tcp.local.']['Version'],
                        request.cls.device_info['_dvl-plcnetapi._tcp.local.']['PlcMacAddress'])


@pytest.fixture()
def mock_plcnet_api(mocker):
    mocker.patch("devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi.__init__", return_value=None)
