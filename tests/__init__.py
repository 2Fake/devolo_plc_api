"""Unittests for devolo_plc_api."""
from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from typing import Any


@dataclass
class TestData:
    """Test data for a devolo device."""

    __test__ = False

    ip: str
    """IP address of a device."""

    device_info: dict[str, dict[str, Any]]
    """Zeroconf info a device delivers."""


def load_test_data():
    """Load test data from file."""
    file = pathlib.Path(__file__).parent / "test_data.json"
    with file.open("r") as handler:
        data = json.load(handler)
    return TestData(ip=data["ip"], device_info=data["device_info"])
