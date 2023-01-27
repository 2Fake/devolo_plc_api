"""Mock methods from the Device class."""
from typing import Any

from devolo_plc_api import Device

from tests import load_test_data


# pylint: disable=unused-argument
def state_change(self: Device, *args: Any, **kwargs: Any) -> None:
    """Evaluate the query result."""
    self._info = load_test_data().device_info
