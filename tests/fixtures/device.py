from asyncio.events import AbstractEventLoop
from copy import deepcopy
from typing import Generator, Type
from unittest.mock import AsyncMock, patch

import pytest

from devolo_plc_api.device import Device

from ..mocks.mock_zeroconf import MockServiceBrowser


@pytest.fixture()
def mock_device(request: pytest.FixtureRequest, event_loop: AbstractEventLoop) -> Generator[Device, None, None]:
    device = Device(ip=request.cls.ip)
    device._info = deepcopy(request.cls.device_info)
    device._loop = event_loop
    device._session = AsyncMock()
    device._zeroconf = AsyncMock()
    yield device


@pytest.fixture()
def mock_service_browser() -> Generator[Type[MockServiceBrowser], None, None]:
    with patch("devolo_plc_api.device.AsyncServiceBrowser", MockServiceBrowser) as asb:
        asb.async_cancel.reset_mock()
        yield asb
