"""Unittests for devolo_plc_api."""
from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass

from devolo_plc_api.device_api import SERVICE_TYPE as DEVICE_API
from devolo_plc_api.plcnet_api import SERVICE_TYPE as PLCNET_API
from devolo_plc_api.zeroconf import ZeroconfServiceInfo


@dataclass
class TestData:
    """Test data for a devolo device."""

    __test__ = False

    ip: str
    """IP address of a device."""

    hostname: str
    """Hostname of a device."""

    device_info: dict[str, ZeroconfServiceInfo]
    """Zeroconf info a device delivers."""


def load_test_data():
    """Load test data from file."""
    file = pathlib.Path(__file__).parent / "test_data.json"
    with file.open("r") as handler:
        data = json.load(handler)
    device_info = {
        DEVICE_API: ZeroconfServiceInfo(hostname=data["hostname"], **data["device_info"][DEVICE_API]),
        PLCNET_API: ZeroconfServiceInfo(**data["device_info"][PLCNET_API]),
    }
    return TestData(ip=data["ip"], hostname=data["hostname"], device_info=device_info)
