"""The devolo device API."""
from .deviceapi import DeviceApi
from .updatefirmware_pb2 import UpdateFirmwareCheck
from .wifinetwork_pb2 import (
    WIFI_BAND_2G,
    WIFI_BAND_5G,
    WIFI_VAP_GUEST_AP,
    WIFI_VAP_MAIN_AP,
    WIFI_VAP_STATION,
    WifiConnectedStationsGet,
    WifiGuestAccessGet,
    WifiNeighborAPsGet,
    WifiRepeatedAPsGet,
)

SERVICE_TYPE = "_dvl-deviceapi._tcp.local."
UPDATE_AVAILABLE = UpdateFirmwareCheck.UPDATE_AVAILABLE
UPDATE_NOT_AVAILABLE = UpdateFirmwareCheck.UPDATE_NOT_AVAILABLE

RepeatedAPInfo = WifiRepeatedAPsGet.RepeatedAPInfo
ConnectedStationInfo = WifiConnectedStationsGet.ConnectedStationInfo
NeighborAPInfo = WifiNeighborAPsGet.NeighborAPInfo

__all__ = [
    "ConnectedStationInfo",
    "DeviceApi",
    "NeighborAPInfo",
    "RepeatedAPInfo",
    "WifiGuestAccessGet",
    "SERVICE_TYPE",
    "UPDATE_AVAILABLE",
    "UPDATE_NOT_AVAILABLE",
    "WIFI_BAND_2G",
    "WIFI_BAND_5G",
    "WIFI_VAP_GUEST_AP",
    "WIFI_VAP_MAIN_AP",
    "WIFI_VAP_STATION",
]
