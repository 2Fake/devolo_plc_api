"""Mock methods from the Device class."""
from typing import Any

from .. import load_test_data


# pylint: disable=protected-access, unused-argument
def state_change(self, *args: Any, **kwargs: Any) -> None:
    """Evaluate the query result."""
    self._info = load_test_data().device_info
