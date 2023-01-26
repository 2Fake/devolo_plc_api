"""Mock methods from the Zeroconf module."""
from __future__ import annotations

from typing import Any, Callable
from unittest.mock import AsyncMock, Mock

from zeroconf import ServiceStateChange, Zeroconf


class MockServiceBrowser:
    """Mock of the ServiceBrowser."""

    _async_start = AsyncMock()
    _async_cancel = AsyncMock()
    async_cancel = AsyncMock()
    cancel = Mock()

    # pylint: disable=unused-argument
    def __init__(self, zeroconf: Zeroconf, type_: str, handlers: list[Callable], **kwargs: Any) -> None:
        """Initialize the service browser."""
        handlers[0](zeroconf, type_, type_, ServiceStateChange.Added)
