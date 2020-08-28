import pytest

from ..mocks.mock_plcnet_api import PlcNetApi


@pytest.fixture()
def mock_plcnet_api(mocker):
    mocker.patch("devolo_plc_api.plcnet_api.plcnetapi.PlcNetApi.__init__", PlcNetApi.__init__)
