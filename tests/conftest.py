"""Test configuration."""
from __future__ import annotations

import asyncio
from typing import Generator
from unittest.mock import AsyncMock, patch

import pytest

from . import TestData, load_test_data

pytest_plugins = [
    "tests.fixtures.device",
    "tests.fixtures.device_api",
    "tests.fixtures.plcnet_api",
    "tests.fixtures.protobuf",
]


@pytest.fixture(scope="session")
def test_data() -> TestData:
    """Load test data."""
    return load_test_data()


@pytest.fixture()
def block_communication() -> Generator[None, None, None]:
    """Block external communication."""
    with patch("devolo_plc_api.device.AsyncZeroconf", new=AsyncMock), patch(
        "devolo_plc_api.device.httpx.AsyncClient", new=AsyncMock
    ), patch("devolo_plc_api.network.Zeroconf"):
        yield


@pytest.fixture()
def event_loop() -> Generator[asyncio.events.AbstractEventLoop, None, None]:
    """Handle the event loop in tests."""
    loop = asyncio.new_event_loop()
    yield loop
    if loop.is_running():
        to_cancel = asyncio.tasks.all_tasks(loop)
        for task in to_cancel:
            task.cancel()
        loop.run_until_complete(asyncio.tasks.gather(*to_cancel, return_exceptions=True))
        loop.close()
