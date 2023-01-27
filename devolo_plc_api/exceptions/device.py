"""Exceptions that can occur when communicating with a devolo device."""


class DeviceNotFound(Exception):
    """The device was not found."""

    def __init__(self, ip: str) -> None:
        """Initialize error."""
        super().__init__(f"The device {ip} did not answer.")


class DeviceUnavailable(Exception):
    """The device is not available, e.g. in standby."""

    def __init__(self) -> None:
        """Initialize error."""
        super().__init__("The device is currently not available. Maybe on standby?")


class DevicePasswordProtected(Exception):
    """The device is password protected."""

    def __init__(self) -> None:
        """Initialize error."""
        super().__init__("The used password is wrong.")
