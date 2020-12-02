import asyncio
from unittest.mock import patch

import pytest
from httpx import AsyncClient, Response

from devolo_plc_api.device_api.deviceapi import DeviceApi

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock


@pytest.fixture()
def device_api(request, feature):
    with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=AsyncMock(return_value=Response)), \
         patch("devolo_plc_api.clients.protobuf.Protobuf._async_post", new=AsyncMock(return_value=Response)), \
         patch("asyncio.get_running_loop", asyncio.new_event_loop):
        asyncio.new_event_loop()
        request.cls.device_info["_dvl-deviceapi._tcp.local."]["properties"]["Features"] = feature
        yield DeviceApi(request.cls.ip, AsyncClient(), request.cls.device_info["_dvl-deviceapi._tcp.local."])


@pytest.fixture()
def mock_device_api(mocker):
    mocker.patch("devolo_plc_api.device_api.deviceapi.DeviceApi.__init__", return_value=None)
