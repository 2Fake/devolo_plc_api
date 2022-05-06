"""Fixture for plcnet API tests."""
from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import AsyncClient

from devolo_plc_api.plcnet_api import SERVICE_TYPE, PlcNetApi

from .. import TestData


@pytest_asyncio.fixture()
async def plcnet_api(test_data: TestData) -> AsyncGenerator[PlcNetApi, None]:
    """Yield prepared PlcNetApi object."""
    async with AsyncClient() as client:
        yield PlcNetApi(test_data.ip, client, test_data.device_info[SERVICE_TYPE])


@pytest.fixture()
def mock_plcnet_api() -> Generator[None, None, None]:
    """Mock PlcNetApi object."""
    with patch("devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi"):
        yield
