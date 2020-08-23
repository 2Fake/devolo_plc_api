import pytest

from ..mocks.mock_zeroconf import _get_zeroconf_info


@pytest.fixture()
def mock_zeroconf(mocker):
    mocker.patch("devolo_plc_api.device.Device._get_zeroconf_info", _get_zeroconf_info)
