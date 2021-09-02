import asyncio
import json
import logging
import pathlib

from httpx import AsyncClient

from devolo_plc_api.clients.protobuf import Protobuf

file = pathlib.Path(__file__).parent / "../test_data.json"
with file.open("r") as fh:
    test_data = json.load(fh)


class StubProtobuf(Protobuf):

    def __init__(self):
        self._logger = logging.getLogger("ProtobufMock")
        self._loop = asyncio.new_event_loop()
        self._ip = test_data["ip"]
        self._port = 14791
        self._session = AsyncClient()
        self._path = test_data["device_info"]["_dvl-plcnetapi._tcp.local."]["properties"]["Path"]
        self._version = test_data["device_info"]["_dvl-plcnetapi._tcp.local."]["properties"]["Version"]
        self._user = "user"

        self.password = "password"
