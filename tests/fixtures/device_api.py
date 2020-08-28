import pytest

from ..mocks.mock_device_api import DeviceApi


@pytest.fixture()
def mock_device_api(mocker):
    mocker.patch("devolo_plc_api.device_api.deviceapi.DeviceApi.__init__", DeviceApi.__init__)
