import pytest

from devolo_plc_api.device import Device


@pytest.fixture()
def mock_device(request):
    device = Device(ip="192.168.0.10")
    device._info = request.cls.device_info
    device._session = None
    return device
