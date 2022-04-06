"""Exceptions that can occur when communicating with a devolo device."""


class DeviceNotFound(Exception):
    """The device was not found."""


class DeviceUnavailable(Exception):
    """The device is not available, e.g. in standby."""


class DevicePasswordProtected(Exception):
    """The device is passwort protected."""
