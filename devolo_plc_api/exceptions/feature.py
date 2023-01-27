"""Exceptions that can occur when determining features."""


class FeatureNotSupported(Exception):
    """The feature is not supported by your device."""

    def __init__(self, feature: str) -> None:
        """Initialize error."""
        super().__init__(f"The device does not support {feature}.")
