import asyncio
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi


@pytest.fixture()
async def plcnet_api(request):
    with patch("asyncio.get_running_loop", asyncio.new_event_loop):
        asyncio.new_event_loop()
        async with AsyncClient() as client:
            plcnet_api = PlcNetApi(request.cls.ip, client, request.cls.device_info["_dvl-plcnetapi._tcp.local."])
            yield plcnet_api


@pytest.fixture()
def mock_plcnet_api(mocker):
    mocker.patch("devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi")
