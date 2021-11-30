from __future__ import annotations

from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from devolo_plc_api.device_api import SERVICE_TYPE, DeviceApi


@pytest.fixture()
async def device_api(request: pytest.FixtureRequest, feature: list[str]) -> AsyncGenerator[DeviceApi, None]:
    request.cls.device_info[SERVICE_TYPE]["properties"]["Features"] = feature
    async with AsyncClient() as client:
        device_api = DeviceApi(request.cls.ip, client, request.cls.device_info[SERVICE_TYPE])
        yield device_api


@pytest.fixture()
def mock_device_api() -> Generator[None, None, None]:
    with patch("devolo_plc_api.device_api.deviceapi.DeviceApi"):
        yield
