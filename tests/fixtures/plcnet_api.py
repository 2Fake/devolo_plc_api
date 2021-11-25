from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from devolo_plc_api.plcnet_api import SERVICE_TYPE, PlcNetApi


@pytest.fixture()
async def plcnet_api(request: pytest.FixtureRequest) -> AsyncGenerator[PlcNetApi, None]:
    async with AsyncClient() as client:
        yield PlcNetApi(request.cls.ip, client, request.cls.device_info[SERVICE_TYPE])


@pytest.fixture()
def mock_plcnet_api() -> Generator[None, None, None]:
    with patch("devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi"):
        yield
