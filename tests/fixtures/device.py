from copy import deepcopy
from unittest.mock import Mock

import pytest
from zeroconf import Zeroconf

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from devolo_plc_api.device import Device

from ..mocks.mock_zeroconf import MockServiceBrowser, MockZeroconf


@pytest.fixture()
def mock_device(request):
    device = Device(ip=request.cls.ip)
    device._info = deepcopy(request.cls.device_info)
    device._loop = Mock()
    device._session = Mock()
    device._session.aclose = AsyncMock()
    device._zeroconf = Mock()
    device._zeroconf.close = lambda: None
    yield device


@pytest.fixture()
def mock_service_browser(mocker):
    mocker.patch("zeroconf.ServiceBrowser.__init__", MockServiceBrowser.__init__)
    mocker.patch("zeroconf.ServiceBrowser.cancel")


@pytest.fixture()
def mock_zeroconf(mocker):
    mocker.patch("zeroconf.Zeroconf.get_service_info", MockZeroconf.get_service_info)
    return Zeroconf()
