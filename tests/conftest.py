"""Test configuration."""
from __future__ import annotations

import asyncio
from typing import Generator
from unittest.mock import AsyncMock, patch

import pytest

from . import TestData, load_test_data
from .mocks.mock_zeroconf import MockServiceBrowser

pytest_plugins = [
    "tests.fixtures.device",
    "tests.fixtures.device_api",
    "tests.fixtures.plcnet_api",
    "tests.fixtures.protobuf",
]


def pytest_configure(config: pytest.Config):
    """Configure pytest."""
    config.addinivalue_line("markers", "allow_sleep: mark tests that are allowed to sleep")


@pytest.fixture(scope="session")
def test_data() -> TestData:
    """Load test data."""
    return load_test_data()


@pytest.fixture(name="sleep", autouse=True)
def patch_sleep(request: pytest.FixtureRequest) -> Generator[AsyncMock | None, None, None]:
    """Don't sleep anywhere except if marked as allowed."""
    if "allow_sleep" not in request.keywords:
        with patch("time.sleep"), patch("asyncio.sleep") as sleep:
            yield sleep
    else:
        yield None


@pytest.fixture()
def block_communication() -> Generator[None, None, None]:
    """Block external communication."""
    with patch("devolo_plc_api.device.AsyncZeroconf", AsyncMock), patch("devolo_plc_api.device.AsyncClient", AsyncMock), patch(
        "devolo_plc_api.device.AsyncServiceBrowser", MockServiceBrowser
    ), patch("devolo_plc_api.device.AsyncServiceInfo"), patch("devolo_plc_api.network.Zeroconf"), patch(
        "devolo_plc_api.network.ServiceBrowser", MockServiceBrowser
    ):
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
