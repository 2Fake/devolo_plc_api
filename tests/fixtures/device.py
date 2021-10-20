from copy import deepcopy
from unittest.mock import Mock, patch

import pytest

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from devolo_plc_api.device import Device

from ..mocks.mock_zeroconf import MockServiceBrowser


@pytest.fixture()
def mock_device(request):
    device = Device(ip=request.cls.ip)
    device._info = deepcopy(request.cls.device_info)
    device._loop = Mock()
    device._session = AsyncMock()
    device._zeroconf = AsyncMock()
    yield device


@pytest.fixture()
def mock_service_browser():
    with patch("devolo_plc_api.device.AsyncServiceBrowser", MockServiceBrowser) as asb:
        asb.async_cancel = AsyncMock()
        yield asb
