"""Test helper methods."""

from syrupy.assertion import SnapshotAssertion

from devolo_plc_api import wifi_qr_code
from devolo_plc_api.device_api.wifinetwork_pb2 import WPA_2, WifiGuestAccessGet


class TestHelpers:
    """Test devolo_plc_api.helpers."""

    def test_wifi_qr_code(self, snapshot: SnapshotAssertion):
        """Test creating a QR code."""
        wifi_guest_access = WifiGuestAccessGet(enabled=True, ssid='"Test"', key='"Test"', wpa=WPA_2)
        assert wifi_qr_code(wifi_guest_access) == snapshot
