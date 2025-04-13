"""Test configuration."""

from __future__ import annotations

from collections import OrderedDict
from functools import partial
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from ifaddr import IP, Adapter

from devolo_plc_api import Device

from . import DeviceType, DifferentDirectoryExtension, TestData, load_test_data
from .mocks.zeroconf import MockAsyncServiceInfo, MockServiceBrowser

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator

    from syrupy.assertion import SnapshotAssertion

pytest_plugins = [
    "tests.fixtures.device_api",
    "tests.fixtures.plcnet_api",
]


@pytest.fixture(scope="session")
def test_data() -> TestData:
    """Load test data."""
    return load_test_data()


@pytest.fixture
def block_communication() -> Generator[None, None, None]:
    """Block external communication."""
    adapter = OrderedDict()
    adapter["eth0"] = Adapter(name="eth0", nice_name="eth0", ips=[IP("192.0.2.100", network_prefix=24, nice_name="eth0")])
    with (
        patch("devolo_plc_api.device.get_adapters", return_value=adapter.values()),
        patch("devolo_plc_api.device.AsyncZeroconf", AsyncMock),
        patch("devolo_plc_api.device.AsyncServiceInfo", MockAsyncServiceInfo),
    ):
        yield


@pytest_asyncio.fixture
async def http_client() -> AsyncGenerator[None, None]:
    """Patch HTTP client."""
    with patch("devolo_plc_api.device.AsyncClient", autospec=True):
        yield


@pytest.fixture
def mock_device(test_data: TestData) -> Device:
    """Generate a device from test data."""
    return Device(ip=test_data.ip)


@pytest.fixture
def mock_info_from_service() -> Generator[Mock, None, None]:
    """Patch reading info from mDNS entries."""
    with patch("devolo_plc_api.device.Device.info_from_service") as ifs:
        yield ifs


@pytest.fixture(name="sleep")
def patch_sleep() -> Generator[AsyncMock, None, None]:
    """Don't sleep anywhere except if marked as allowed."""
    with patch("time.sleep"), patch("asyncio.sleep") as sleep:
        yield sleep


@pytest.fixture
def service_browser(device_type: DeviceType) -> Generator[None, None, None]:
    """Patch mDNS service browser."""
    service_browser = partial(MockServiceBrowser, device_type=device_type)
    with (
        patch("devolo_plc_api.device.AsyncServiceBrowser", service_browser),
        patch("devolo_plc_api.network.ServiceBrowser", service_browser),
    ):
        yield


@pytest.fixture
def snapshot(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with nicer path."""
    return snapshot.use_extension(DifferentDirectoryExtension)
