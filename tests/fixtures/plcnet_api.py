import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi


@pytest.fixture()
async def plcnet_api(request: pytest.FixtureRequest) -> AsyncGenerator[PlcNetApi, None]:
    with patch("asyncio.get_running_loop", asyncio.new_event_loop):
        asyncio.new_event_loop()
        async with AsyncClient() as client:
            yield PlcNetApi(request.cls.ip, client, request.cls.device_info["_dvl-plcnetapi._tcp.local."])


@pytest.fixture()
def mock_plcnet_api() -> Generator[None, None, None]:
    with patch("devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi"):
        yield
