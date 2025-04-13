"""The devolo plcnet API."""

from .getnetworkoverview_pb2 import GetNetworkOverview
from .plcnetapi import PlcNetApi

DEVICES_WITHOUT_PLCNET = ["3046", "3047", "3048", "3049", "3254", "3255", "3256"]
GHN_SPIRIT = GetNetworkOverview.Device.GHN_SPIRIT
HPAV_PANTHER = GetNetworkOverview.Device.HPAV_PANTHER
HPAV_THUNDERBOLT = GetNetworkOverview.Device.HPAV_THUNDERBOLT
LOCAL = GetNetworkOverview.Device.LOCAL
REMOTE = GetNetworkOverview.Device.REMOTE
SERVICE_TYPE = "_dvl-plcnetapi._tcp.local."

DataRate = GetNetworkOverview.DataRate
Device = GetNetworkOverview.Device
LogicalNetwork = GetNetworkOverview.LogicalNetwork

__all__ = [
    "DEVICES_WITHOUT_PLCNET",
    "GHN_SPIRIT",
    "HPAV_PANTHER",
    "HPAV_THUNDERBOLT",
    "LOCAL",
    "REMOTE",
    "SERVICE_TYPE",
    "DataRate",
    "Device",
    "LogicalNetwork",
    "PlcNetApi",
]
