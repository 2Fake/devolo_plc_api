"""Test helper methods."""
from devolo_plc_api import wifi_qr_code
from devolo_plc_api.device_api.wifinetwork_pb2 import WPA_2, WifiGuestAccessGet


class TestHelpers:
    """Test devolo_plc_api.helpers."""

    def test_wifi_qr_code(self):
        """Test getting wifi guest access status asynchronously."""
        wifi_guest_access = WifiGuestAccessGet(enabled=True, ssid='"Test"', key='"Test"', wpa=WPA_2)
        assert (
            wifi_qr_code(wifi_guest_access)
            == b'<?xml version="1.0" encoding="utf-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="37" height="37" '
            b'class="segno"><path class="qrline" stroke="#000" d="M4 4.5h7m2 0h1m1 0h1m2 0h1m7 0h7m-29 1h1m5 0h1m2 0h1m6 '
            b"0h2m2 0h1m1 0h1m5 0h1m-29 1h1m1 0h3m1 0h1m2 0h1m1 0h1m2 0h2m1 0h3m2 0h1m1 0h3m1 0h1m-29 1h1m1 0h3m1 0h1m3 "
            b"0h2m1 0h1m6 0h1m1 0h1m1 0h3m1 0h1m-29 1h1m1 0h3m1 0h1m3 0h1m1 0h1m4 0h1m2 0h1m1 0h1m1 0h3m1 0h1m-29 1h1m5 "
            b"0h1m1 0h2m5 0h1m1 0h1m1 0h2m1 0h1m5 0h1m-29 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-17 1h2m1 "
            b"0h3m1 0h1m-20 1h1m2 0h1m1 0h2m1 0h2m4 0h1m1 0h2m3 0h1m1 0h1m-24 1h5m4 0h3m1 0h1m1 0h1m2 0h1m3 0h2m1 0h3m-28 "
            b"1h1m1 0h1m2 0h2m1 0h1m2 0h4m1 0h1m2 0h2m1 0h2m2 0h2m-28 1h1m1 0h3m3 0h2m1 0h3m5 0h1m1 0h2m2 0h4m-29 1h1m5 "
            b"0h1m1 0h1m1 0h1m3 0h2m1 0h3m1 0h5m1 0h2m-29 1h5m2 0h1m4 0h3m1 0h2m2 0h1m1 0h1m3 0h3m-29 1h2m4 0h2m1 0h1m2 "
            b"0h3m3 0h1m2 0h1m4 0h3m-26 1h1m1 0h1m2 0h5m4 0h1m1 0h3m1 0h2m-25 1h2m1 0h1m2 0h3m1 0h1m1 0h2m1 0h2m2 0h1m3 "
            b"0h1m2 0h1m1 0h1m-28 1h3m1 0h1m1 0h1m1 0h6m3 0h1m2 0h2m3 0h2m-28 1h1m1 0h5m1 0h1m5 0h1m1 0h1m5 0h3m1 0h3m-27 "
            b"1h1m1 0h1m2 0h3m1 0h2m1 0h1m1 0h2m1 0h1m1 0h1m1 0h1m-24 1h1m1 0h1m3 0h1m1 0h1m1 0h1m1 0h1m3 0h1m3 0h9m-21 "
            b"1h5m1 0h1m2 0h1m2 0h1m3 0h3m-27 1h7m2 0h2m1 0h1m7 0h1m1 0h1m1 0h2m1 0h1m-28 1h1m5 0h1m1 0h1m5 0h3m1 0h1m1 "
            b"0h1m3 0h1m1 0h3m-29 1h1m1 0h3m1 0h1m2 0h4m2 0h1m1 0h1m2 0h7m1 0h1m-29 1h1m1 0h3m1 0h1m1 0h1m1 0h1m2 0h1m1 "
            b"0h1m1 0h3m2 0h2m1 0h1m1 0h1m-28 1h1m1 0h3m1 0h1m2 0h2m3 0h1m1 0h1m1 0h2m1 0h2m1 0h3m1 0h1m-29 1h1m5 0h1m2 "
            b'0h2m1 0h1m2 0h6m2 0h1m3 0h1m-28 1h7m1 0h1m2 0h1m1 0h1m2 0h2m2 0h1m3 0h1m1 0h2"/></svg>\n'
        )
