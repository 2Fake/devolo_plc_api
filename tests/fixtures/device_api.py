from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from devolo_plc_api.device_api.deviceapi import DeviceApi


@pytest.fixture()
async def device_api(request: pytest.FixtureRequest, feature: list[str]) -> AsyncGenerator[DeviceApi, None]:
    with patch("asyncio.get_running_loop", asyncio.new_event_loop):
        request.cls.device_info["_dvl-deviceapi._tcp.local."]["properties"]["Features"] = feature
        async with AsyncClient() as client:
            device_api = DeviceApi(request.cls.ip, client, request.cls.device_info["_dvl-deviceapi._tcp.local."])
            yield device_api


@pytest.fixture()
def mock_device_api() -> Generator[None, None, None]:
    with patch("devolo_plc_api.device_api.deviceapi.DeviceApi"):
        yield
