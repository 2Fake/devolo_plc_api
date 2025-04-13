"""Helper methods to allow advanced usage of information provided by the device."""

from io import BytesIO
from typing import Any

from segno.helpers import make_wifi

from devolo_plc_api.device_api import WifiGuestAccessGet
from devolo_plc_api.device_api.wifinetwork_pb2 import WPA_NONE


def wifi_qr_code(guest_wifi: WifiGuestAccessGet, kind: str = "svg", **kwargs: Any) -> bytes:
    """
    Generate a wifi QR code.

    :param guest_wifi: Wifi credentials to represent in the QR code
    :param kind: Output format of the image
    :return: Bytes of image
    """
    buffer = BytesIO()
    qr_code = make_wifi(ssid=guest_wifi.ssid, password=guest_wifi.key, security=None if guest_wifi.wpa == WPA_NONE else "WPA")
    qr_code.save(out=buffer, kind=kind, **kwargs)
    return buffer.getvalue()
