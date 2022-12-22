"""The devolo device API."""
from .deviceapi import DeviceApi
from .updatefirmware_pb2 import UpdateFirmwareCheck
from .wifinetwork_pb2 import WifiConnectedStationsGet, WifiGuestAccessGet, WifiNeighborAPsGet, WifiRepeatedAPsGet

SERVICE_TYPE = "_dvl-deviceapi._tcp.local."

RepeatedAPInfo = WifiRepeatedAPsGet.RepeatedAPInfo
ConnectedStationInfo = WifiConnectedStationsGet.ConnectedStationInfo
NeighborAPInfo = WifiNeighborAPsGet.NeighborAPInfo

__all__ = [
    "ConnectedStationInfo",
    "DeviceApi",
    "NeighborAPInfo",
    "RepeatedAPInfo",
    "UpdateFirmwareCheck",
    "WifiGuestAccessGet",
]
