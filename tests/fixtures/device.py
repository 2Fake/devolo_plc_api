from copy import deepcopy

import pytest
from zeroconf import Zeroconf

from devolo_plc_api.device import Device

from ..mocks.mock_zeroconf import MockZeroconf


@pytest.fixture()
def mock_device(request):
    device = Device(ip=request.cls.ip)
    device._info = deepcopy(request.cls.device_info)
    device._session = None
    device._zeroconf = None
    return device


@pytest.fixture()
def mock_service_browser(mocker):
    mocker.patch("zeroconf.ServiceBrowser.__init__", return_value=None)
    mocker.patch("zeroconf.ServiceBrowser.cancel", return_value=None)


@pytest.fixture()
def mock_zeroconf(mocker):
    mocker.patch("zeroconf.Zeroconf.get_service_info", MockZeroconf.get_service_info)
    return Zeroconf()
