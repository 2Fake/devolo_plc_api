"""Stubs for the zeroconf module."""
import socket
from unittest.mock import AsyncMock

from zeroconf.asyncio import AsyncServiceInfo

from devolo_plc_api.plcnet_api import SERVICE_TYPE

from .. import load_test_data


class StubAsyncServiceInfo(AsyncServiceInfo):
    """AsyncServiceInfo object with pre-filled information."""

    async_request = AsyncMock()

    def __init__(self, service_type: str, name: str) -> None:
        test_data = load_test_data()
        super().__init__(service_type, name, addresses=[socket.inet_aton(test_data.ip)])
        self.server = test_data.hostname
        self.text = b"\x1aPlcMacAddress=" + test_data.device_info[SERVICE_TYPE].properties["PlcMacAddress"].encode()
