"""Fixtures to properly mock a devolo device."""
from typing import Generator, Type
from unittest.mock import patch

import pytest

from devolo_plc_api import Device
from devolo_plc_api.device_api import SERVICE_TYPE as DEVICEAPI
from devolo_plc_api.plcnet_api import SERVICE_TYPE as PLCNETAPI

from .. import TestData
from ..mocks.mock_zeroconf import MockServiceBrowser


@pytest.fixture()
def mock_device(test_data: TestData) -> Generator[Device, None, None]:
    """Generate device from test data."""
    yield Device(ip=test_data.ip, plcnetapi=test_data.device_info[PLCNETAPI], deviceapi=test_data.device_info[DEVICEAPI])


@pytest.fixture()
def mock_service_browser() -> Generator[Type[MockServiceBrowser], None, None]:
    """Patch zeroconf service browser."""
    with patch("devolo_plc_api.device.AsyncServiceBrowser", MockServiceBrowser) as asb:
        asb.async_cancel.reset_mock()
        yield asb
