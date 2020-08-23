from aiohttp import ClientSession

from ..clients.protobuf import Protobuf
from . import devolo_idl_proto_plcnetapi_getnetworkoverview_pb2


class PlcNetApi(Protobuf):
    """
    Implementation of the devolo plcnet API.

    :param ip: IP address of the device to communicate with
    :param session: HTTP client session
    :param path: Path to send queries to
    :param version: Version of the API to use
    """

    def __init__(self, ip: str, session: ClientSession, path: str, version: str):
        self._ip = ip
        self._port = 47219
        self._session = session
        self._path = path
        self._version = version


    async def get_network_overview(self) -> dict:
        """ Get a PLC network overview. """
        network_overview = devolo_idl_proto_plcnetapi_getnetworkoverview_pb2.GetNetworkOverview()
        responds = await self.get("GetNetworkOverview")
        network_overview.ParseFromString(await responds.read())
        return network_overview
