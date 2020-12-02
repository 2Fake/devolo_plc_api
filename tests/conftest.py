import json
import pathlib

import pytest

pytest_plugins = [
    'tests.fixtures.device',
    'tests.fixtures.device_api',
    'tests.fixtures.plcnet_api',
    'tests.fixtures.protobuf',
]

file = pathlib.Path(__file__).parent / "test_data.json"
with file.open("r") as fh:
    test_data = json.load(fh)


@pytest.fixture(autouse=True, scope="class")
def test_data_fixture(request):
    """ Load test data. """
    request.cls.device_info = test_data['device_info']
    request.cls.ip = test_data['ip']
