"""Fixtures to properly mock a devolo device."""
from __future__ import annotations

from typing import Generator
from unittest.mock import AsyncMock, Mock, patch

import pytest

from devolo_plc_api import Device

from tests import TestData
from tests.mocks.mock_zeroconf import MockServiceBrowser


@pytest.fixture()
def mock_async_request() -> Generator[AsyncMock, None, None]:
    """Patch requesting mDNS data."""
    with patch("devolo_plc_api.device.AsyncServiceInfo.async_request") as ar:
        yield ar


@pytest.fixture()
def mock_device(test_data: TestData) -> Device:
    """Generate a device from test data."""
    device = Device(ip=test_data.ip)
    device._info = test_data.device_info
    return device


@pytest.fixture()
def mock_get_device_info() -> Generator[AsyncMock, None, None]:
    """Patch getting device info."""
    with patch("devolo_plc_api.device.Device._get_device_info") as gdi:
        yield gdi


@pytest.fixture()
def mock_get_zeroconf_info() -> Generator[AsyncMock, None, None]:
    """Patch getting zeroconf info."""
    with patch("devolo_plc_api.device.Device._get_zeroconf_info") as gzi:
        yield gzi


@pytest.fixture()
def mock_info_from_service() -> Generator[Mock, None, None]:
    """Patch reading info from mDNS entries."""
    with patch("devolo_plc_api.device.Device.info_from_service") as ifs:
        yield ifs


@pytest.fixture()
def mock_service_browser() -> Generator[type[MockServiceBrowser], None, None]:
    """Patch zeroconf service browser."""
    with patch("devolo_plc_api.device.AsyncServiceBrowser", MockServiceBrowser) as asb:
        asb.async_cancel.reset_mock()
        yield asb
