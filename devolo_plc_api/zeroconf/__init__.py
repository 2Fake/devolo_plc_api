"""Zeroconf dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ZeroconfServiceInfo:
    """Prepared info from mDNS entries."""

    address: bytes = b""
    """IP address of the device."""

    port: int | None = None
    """mDNS port to use."""

    hostname: str = ""
    """mDNS hostname of the device."""

    properties: dict[str, str] = field(default_factory=dict)
    """Properties provided by the device."""
