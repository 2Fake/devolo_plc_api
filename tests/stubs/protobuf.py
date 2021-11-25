import asyncio
import json
import logging
import pathlib

from httpx import AsyncClient

from devolo_plc_api.clients.protobuf import Protobuf
from devolo_plc_api.plcnet_api import SERVICE_TYPE

file = pathlib.Path(__file__).parent / "../test_data.json"
with file.open("r") as fh:
    test_data = json.load(fh)


class StubProtobuf(Protobuf):

    def __init__(self) -> None:
        self._logger = logging.getLogger("ProtobufMock")
        self._ip = test_data["ip"]
        self._port = 14791
        self._session = AsyncClient()
        self._path = test_data["device_info"][SERVICE_TYPE]["properties"]["Path"]
        self._version = test_data["device_info"][SERVICE_TYPE]["properties"]["Version"]
        self._user = "user"

        self.password = "password"
