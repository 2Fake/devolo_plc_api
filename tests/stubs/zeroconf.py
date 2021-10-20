import json
import pathlib
import socket

from zeroconf.asyncio import AsyncServiceInfo

file = pathlib.Path(__file__).parent / ".." / "test_data.json"
with file.open("r") as fh:
    test_data = json.load(fh)


class StubAsyncServiceInfo(AsyncServiceInfo):

    def __init__(self, service_type, name):
        super().__init__(service_type, name, addresses=[socket.inet_aton(test_data['ip'])])
        self.text = b"\x09new=value"
