"""Fixture for device API tests."""
from __future__ import annotations

from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import AsyncClient

from devolo_plc_api.device_api import SERVICE_TYPE, DeviceApi

from .. import TestData


@pytest_asyncio.fixture()
async def device_api(test_data: TestData, feature: str) -> AsyncGenerator[DeviceApi, None]:
    """Yield prepared DeviceApi object."""
    test_data.device_info[SERVICE_TYPE]["properties"]["Features"] = feature
    async with AsyncClient() as client:
        yield DeviceApi(test_data.ip, client, test_data.device_info[SERVICE_TYPE])


@pytest.fixture()
def mock_device_api() -> Generator[None, None, None]:
    """Mock DeviceApi object."""
    with patch("devolo_plc_api.device_api.deviceapi.DeviceApi"):
        yield
