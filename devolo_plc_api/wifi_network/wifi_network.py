from . import devolo_idl_proto_deviceapi_wifinetwork_pb2
from ..protobuf_sender import ProtobufSender


class WifiNetwork(ProtobufSender):
    def __init__(self, ip: str, session, port):
        super().__init__(ip, session, port)

    async def get_wifi_guest_access(self):
        wifi_guest_proto = devolo_idl_proto_deviceapi_wifinetwork_pb2.WifiGuestAccessGet()
        r = await self.get("WifiGuestAccessGet")
        wifi_guest_proto.ParseFromString(await r.read())
        return wifi_guest_proto
