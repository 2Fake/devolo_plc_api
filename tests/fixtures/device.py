from copy import deepcopy
from unittest.mock import Mock

import pytest
from zeroconf import Zeroconf

from devolo_plc_api.device import Device

from ..mocks.mock_zeroconf import MockServiceBrowser, MockZeroconf


@pytest.fixture()
def mock_device(mocker, request):
    device = Device(ip=request.cls.ip)
    device._info = deepcopy(request.cls.device_info)
    device._loop = Mock()
    device._loop.is_running = lambda: False
    device._session = None
    device._zeroconf = None
    return device


@pytest.fixture()
def mock_service_browser(mocker):
    mocker.patch("zeroconf.ServiceBrowser.__init__", MockServiceBrowser.__init__)
    mocker.patch("zeroconf.ServiceBrowser.cancel", return_value=None)


@pytest.fixture()
def mock_zeroconf(mocker):
    mocker.patch("zeroconf.Zeroconf.get_service_info", MockZeroconf.get_service_info)
    return Zeroconf()
