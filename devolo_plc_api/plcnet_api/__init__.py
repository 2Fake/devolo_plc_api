"""The devolo plcnet API."""
from .getnetworkoverview_pb2 import GetNetworkOverview
from .plcnetapi import PlcNetApi

DEVICES_WITHOUT_PLCNET = [3046, 3047, 3048, 3049, 3254, 3255, 3256]
SERVICE_TYPE = "_dvl-plcnetapi._tcp.local."

Device = GetNetworkOverview.Device
LogicalNetwork = GetNetworkOverview.LogicalNetwork

__all__ = ["Device", "LogicalNetwork", "PlcNetApi"]
