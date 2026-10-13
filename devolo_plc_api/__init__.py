"""The devolo PLC API."""

from importlib.metadata import PackageNotFoundError, version

from .device import Device
from .postprocessing import hops, lost_maps, neighboring_plc_networks, temperature, wifi_qr_code, wire_length

try:
    __version__ = version("devolo_plc_api")
except PackageNotFoundError:
    # package is not installed - e.g. pulled and run locally
    __version__ = "0.0.0"

__all__ = [
    "Device",
    "__version__",
    "hops",
    "lost_maps",
    "neighboring_plc_networks",
    "temperature",
    "wifi_qr_code",
    "wire_length",
]
