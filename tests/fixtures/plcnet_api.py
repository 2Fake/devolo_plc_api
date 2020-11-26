import asyncio
from unittest.mock import patch

import pytest
from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi
from httpx import AsyncClient, Response

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock


@pytest.fixture()
def plcnet_api(request):
    with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
         patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)), \
         patch("asyncio.get_running_loop", asyncio.new_event_loop):
        asyncio.new_event_loop()
        yield PlcNetApi(request.cls.ip,
                        AsyncClient(),
                        request.cls.device_info["_dvl-plcnetapi._tcp.local."])


@pytest.fixture()
def mock_plcnet_api(mocker):
    mocker.patch("devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi.__init__", return_value=None)
