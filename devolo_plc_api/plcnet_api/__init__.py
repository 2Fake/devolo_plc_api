"""The devolo plcnet API."""
from .plcnetapi import PlcNetApi

DEVICES_WITHOUT_PLCNET = [3046, 3047, 3048, 3049, 3254, 3255]
SERVICE_TYPE = "_dvl-plcnetapi._tcp.local."

__all__ = ["PlcNetApi"]
