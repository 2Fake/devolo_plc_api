from .network_overview.network_overview import NetworkOverview
from ..helper.zeroconf import get_token


class PlcNetApi(NetworkOverview):
    def __init__(self, ip, session):
        self.token = get_token(ip, "_dvl-plcnetapi._tcp.local.")
        super().__init__(ip=ip, session=session, port=47219, token=self.token)
