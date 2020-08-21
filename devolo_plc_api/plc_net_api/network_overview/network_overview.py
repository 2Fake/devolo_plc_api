from devolo_plc_api.plc_net_api.network_overview import devolo_idl_proto_plcnetapi_getnetworkoverview_pb2
from devolo_plc_api.protobuf_sender import ProtobufSender


class NetworkOverview(ProtobufSender):
    def __init__(self, ip: str, session, port, token):
        super().__init__(ip=ip,
                         session=session,
                         port=port,
                         api_type="plcnetapi",
                         token=token)

    async def get_network_overview(self):
        network_overview = devolo_idl_proto_plcnetapi_getnetworkoverview_pb2.GetNetworkOverview()
        r = await self.get("GetNetworkOverview")
        network_overview.ParseFromString(await r.read())
        return network_overview
