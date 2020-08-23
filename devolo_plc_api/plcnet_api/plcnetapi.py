from ..clients.protobuf import Protobuf
from . import devolo_idl_proto_plcnetapi_getnetworkoverview_pb2


class PlcNetApi(Protobuf):
    def __init__(self, ip, session, path, version):
        self._ip = ip
        self._port = 47219
        self._session = session
        self._path = path
        self._version = version


    async def get_network_overview(self):
        network_overview = devolo_idl_proto_plcnetapi_getnetworkoverview_pb2.GetNetworkOverview()
        responds = await self.get("GetNetworkOverview")
        network_overview.ParseFromString(await responds.read())
        return network_overview
