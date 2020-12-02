import json
import pathlib

file = pathlib.Path(__file__).parent / ".." / "test_data.json"
with file.open("r") as fh:
    test_data = json.load(fh)


def state_change(self):
    self._info = test_data["device_info"]
