"""Helper methods to allow advanced usage of information provided by the device."""
from io import BytesIO

from segno.helpers import make_wifi

from devolo_plc_api.device_api import WifiGuestAccessGet
from devolo_plc_api.device_api.wifinetwork_pb2 import WPA_NONE


def wifi_qr_code(guest_wifi: WifiGuestAccessGet) -> bytes:
    """Generate a wifi QR code."""
    buffer = BytesIO()
    qr_code = make_wifi(ssid=guest_wifi.ssid, password=guest_wifi.key, security=None if guest_wifi.wpa == WPA_NONE else "WPA")
    qr_code.save(out=buffer, kind="svg")
    return buffer.getvalue()
