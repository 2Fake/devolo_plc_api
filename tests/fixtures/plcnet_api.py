"""Fixtures for plcnet API tests."""

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from devolo_plc_api.plcnet_api import SERVICE_TYPE, LogicalNetwork, PlcNetApi

from tests import TestData


@pytest_asyncio.fixture()
async def plcnet_api(test_data: TestData) -> AsyncGenerator[PlcNetApi, None]:
    """Yield a prepared PlcNetApi object."""
    async with AsyncClient() as client:
        yield PlcNetApi(test_data.ip, client, test_data.device_info[SERVICE_TYPE])


@pytest.fixture
def network() -> LogicalNetwork:
    """Mock a PLC network."""
    return LogicalNetwork(devices=[], data_rates=[])
