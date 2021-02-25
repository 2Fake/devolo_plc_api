import asyncio
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from devolo_plc_api.device_api.deviceapi import DeviceApi


@pytest.fixture()
async def device_api(request, feature):
    with patch("asyncio.get_running_loop", asyncio.new_event_loop):
        request.cls.device_info["_dvl-deviceapi._tcp.local."]["properties"]["Features"] = feature
        async with AsyncClient() as client:
            device_api = DeviceApi(request.cls.ip, client, request.cls.device_info["_dvl-deviceapi._tcp.local."])
            yield device_api


@pytest.fixture()
def mock_device_api(mocker):
    mocker.patch("devolo_plc_api.device_api.deviceapi.DeviceApi")
