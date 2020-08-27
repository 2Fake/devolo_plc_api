import pytest

from devolo_plc_api.device import Device
from ..mocks.mock_service_browser import ServiceBrowser


@pytest.fixture()
def mock_device(request):
    device = Device(ip="192.168.0.10")
    device._info = request.cls.device_info
    device._session = None
    device._zeroconf = None
    return device


@pytest.fixture()
def mock_service_browser(mocker):
    mocker.patch("zeroconf.ServiceBrowser.__init__", ServiceBrowser.__init__)
    mocker.patch("zeroconf.ServiceBrowser.cancel", ServiceBrowser.cancel)
