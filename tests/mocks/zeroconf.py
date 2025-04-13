"""Mock methods from the Zeroconf module."""

from __future__ import annotations

import socket
from typing import Any, Callable
from unittest.mock import AsyncMock, Mock

from zeroconf import ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceInfo

from devolo_plc_api.plcnet_api import SERVICE_TYPE

from tests import DeviceType, load_test_data


class MockServiceBrowser:
    """Mock of the ServiceBrowser."""

    _async_start = AsyncMock()
    _async_cancel = AsyncMock()
    async_cancel = AsyncMock()
    cancel = Mock()

    def __init__(self, zeroconf: Zeroconf, type_: list[str] | str, handlers: list[Callable], **kwargs: Any) -> None:
        """Initialize the service browser."""
        if isinstance(type_, str):
            type_ = [type_]
        elif kwargs.get("device_type") == DeviceType.REPEATER:
            type_.remove(SERVICE_TYPE)
        for service_type in type_:
            handlers[0](zeroconf, service_type, service_type, ServiceStateChange.Added)


class MockAsyncServiceInfo(AsyncServiceInfo):
    """AsyncServiceInfo object with pre-filled information."""

    async_request = AsyncMock()

    def __init__(self, service_type: str, name: str) -> None:
        """Initialize the service info."""
        test_data = load_test_data()
        super().__init__(
            service_type,
            name,
            port=test_data.device_info[service_type].port,
            properties=test_data.device_info[service_type].properties,
            server=test_data.hostname,
            addresses=[socket.inet_aton(test_data.ip)],
        )
