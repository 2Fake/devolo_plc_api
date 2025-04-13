"""Fixtures for device API tests."""

from __future__ import annotations

from secrets import randbelow
from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from httpx import AsyncClient

from devolo_plc_api.device_api import (
    SERVICE_TYPE,
    ConnectedStationInfo,
    DeviceApi,
    NeighborAPInfo,
    RepeatedAPInfo,
    SupportInfoItem,
    UpdateFirmwareCheck,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from tests import TestData


@pytest_asyncio.fixture
async def device_api(test_data: TestData, feature: str) -> AsyncGenerator[DeviceApi, None]:
    """Yield a prepared DeviceApi object."""
    test_data.device_info[SERVICE_TYPE].properties["Features"] = feature
    async with AsyncClient() as client:
        yield DeviceApi(test_data.ip, client, test_data.device_info[SERVICE_TYPE])


@pytest.fixture(scope="session")
def connected_station() -> ConnectedStationInfo:
    """Generate a mocked answer of a connected wifi station."""
    station = ConnectedStationInfo()
    station.mac_address = "aa:bb:cc:dd:ee:ff"
    return station


@pytest.fixture(scope="session")
def firmware_update() -> UpdateFirmwareCheck:
    """Generate a mocked firmware update message."""
    update = UpdateFirmwareCheck()
    update.result = UpdateFirmwareCheck.UPDATE_NOT_AVAILABLE
    update.new_firmware_version = ""
    return update


@pytest.fixture(scope="session")
def neighbor_ap() -> NeighborAPInfo:
    """Generate a mocked answer of a neighbor access point."""
    ap = NeighborAPInfo()
    ap.mac_address = "aa:bb:cc:dd:ee:ff"
    return ap


@pytest.fixture(scope="session")
def repeated_ap() -> RepeatedAPInfo:
    """Generate a mocked answer of a repeated access point."""
    ap = RepeatedAPInfo()
    ap.mac_address = "aa:bb:cc:dd:ee:ff"
    return ap


@pytest.fixture(scope="session")
def runtime() -> int:
    """Generate a mocked runtime of a device."""
    return randbelow(65536)


@pytest.fixture(scope="session")
def support_item() -> SupportInfoItem:
    """Generate mocked support information."""
    return SupportInfoItem(label="test", content=b"test")
