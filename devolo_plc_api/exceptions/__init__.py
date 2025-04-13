"""Exceptions used by the package."""

from .device import DeviceNotFound, DevicePasswordProtected, DeviceUnavailable
from .feature import FeatureNotSupported

__all__ = ["DeviceNotFound", "DevicePasswordProtected", "DeviceUnavailable", "FeatureNotSupported"]
