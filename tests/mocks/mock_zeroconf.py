import json
import pathlib
import socket

from zeroconf import ServiceInfo

file = pathlib.Path(__file__).parent / ".." / "test_data.json"
with file.open("r") as fh:
    test_data = json.load(fh)


class MockZeroconf:

    def get_service_info(self, service_type, name):
        service_info = ServiceInfo(service_type, name)
        service_info.addresses = [socket.inet_aton(test_data['ip'])]
        service_info.text = b"\x09new=value"
        return service_info


class MockServiceBrowser:

    def __init__(self, zc, st, sc, addr=None):
        sc[0]()
