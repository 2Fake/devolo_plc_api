"""Stubs for the protobuf class."""
from httpx import AsyncClient

from devolo_plc_api.clients.protobuf import Protobuf
from devolo_plc_api.plcnet_api import SERVICE_TYPE

from .. import load_test_data


class StubProtobuf(Protobuf):
    """Protobuf object with pre-filled information."""

    def __init__(self) -> None:
        test_data = load_test_data()
        super().__init__()
        self._ip = test_data.ip
        self._port = 14791
        self._session = AsyncClient()
        self._path = test_data.device_info[SERVICE_TYPE]["properties"]["Path"]
        self._version = test_data.device_info[SERVICE_TYPE]["properties"]["Version"]
        self._user = "user"

        self.password = "password"

    async def close_session(self) -> None:
        """Close HTTP session."""
        await self._session.aclose()
