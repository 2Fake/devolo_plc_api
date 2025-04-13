"""The devolo device API."""

import re

from .deviceapi import DeviceApi
from .multiap_pb2 import WifiMultiApGetResponse
from .support_pb2 import SupportInfoDump
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

CONFIGLAYER_FORMAT = re.compile(rb"(([A-Z][A-Z0-9._]+)=(.+?))(?=(([A-Z][A-Z0-9._]+)=(.+))|$)", re.DOTALL)
SERVICE_TYPE = "_dvl-deviceapi._tcp.local."
UPDATE_AVAILABLE = UpdateFirmwareCheck.UPDATE_AVAILABLE
UPDATE_NOT_AVAILABLE = UpdateFirmwareCheck.UPDATE_NOT_AVAILABLE

RepeatedAPInfo = WifiRepeatedAPsGet.RepeatedAPInfo
ConnectedStationInfo = WifiConnectedStationsGet.ConnectedStationInfo
NeighborAPInfo = WifiNeighborAPsGet.NeighborAPInfo
SupportInfoItem = SupportInfoDump.SupportInfoItem

__all__ = [
    "CONFIGLAYER_FORMAT",
    "SERVICE_TYPE",
    "UPDATE_AVAILABLE",
    "UPDATE_NOT_AVAILABLE",
    "WIFI_BAND_2G",
    "WIFI_BAND_5G",
    "WIFI_VAP_GUEST_AP",
    "WIFI_VAP_MAIN_AP",
    "WIFI_VAP_STATION",
    "ConnectedStationInfo",
    "DeviceApi",
    "NeighborAPInfo",
    "RepeatedAPInfo",
    "SupportInfoItem",
    "WifiGuestAccessGet",
    "WifiMultiApGetResponse",
]
