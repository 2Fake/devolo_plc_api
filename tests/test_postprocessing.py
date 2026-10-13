"""Test postprocessing of information provided by the device."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from syrupy.assertion import SnapshotAssertion

from devolo_plc_api import hops, lost_maps, neighboring_plc_networks, temperature, wifi_qr_code, wire_length
from devolo_plc_api.device_api.wifinetwork_pb2 import WPA_2, WifiGuestAccessGet

if TYPE_CHECKING:
    from collections.abc import Callable

    from devolo_plc_api.device_api import SupportInfoDump

VALUE_FUNCTIONS = [hops, lost_maps, neighboring_plc_networks, temperature, wire_length]


class TestQrCode:
    """Test devolo_plc_api.postprocessing.qrcode."""

    def test_wifi_qr_code(self, snapshot: SnapshotAssertion):
        """Test creating a QR code."""
        wifi_guest_access = WifiGuestAccessGet(enabled=True, ssid='"Test"', key='"Test"', wpa=WPA_2)
        assert wifi_qr_code(wifi_guest_access) == snapshot


class TestSupportInfo:
    """Test devolo_plc_api.postprocessing.supportinfo."""

    @pytest.mark.parametrize("node_type", ["END_POINT"])
    def test_temperature(self, support_info: SupportInfoDump):
        """Test getting the temperature of the G.hn PLC chip."""
        assert temperature(support_info) == 70.9

    @pytest.mark.parametrize("node_type", ["END_POINT"])
    def test_neighboring_plc_networks(self, support_info: SupportInfoDump):
        """Test getting the number of neighboring PLC networks."""
        assert neighboring_plc_networks(support_info) == 1

    @pytest.mark.parametrize(("node_type", "expected"), [("END_POINT", 1), ("DOMAIN_MASTER", 0)])
    def test_hops(self, support_info: SupportInfoDump, expected: int):
        """Test getting the number of hops to the domain master."""
        assert hops(support_info) == expected

    @pytest.mark.parametrize(("node_type", "expected"), [("END_POINT", 178), ("DOMAIN_MASTER", 0)])
    def test_lost_maps(self, support_info: SupportInfoDump, expected: int):
        """Test getting the number of lost media access plans."""
        assert lost_maps(support_info) == expected

    @pytest.mark.parametrize("node_type", ["END_POINT"])
    def test_wire_length(self, support_info: SupportInfoDump):
        """Test getting the length of the power line to the uplink device."""
        assert wire_length(support_info) == 97

    @pytest.mark.parametrize("node_type", ["DOMAIN_MASTER", "ALONE"])
    def test_wire_length_without_uplink(self, support_info: SupportInfoDump):
        """Test getting no length of the power line, if a device has no uplink."""
        assert wire_length(support_info) is None

    @pytest.mark.parametrize("value_func", VALUE_FUNCTIONS)
    def test_unsupported_firmware(
        self, unsupported_support_info: SupportInfoDump, value_func: Callable[[SupportInfoDump], float | None]
    ):
        """Test handling support information not holding any known value."""
        assert value_func(unsupported_support_info) is None

    @pytest.mark.parametrize("value_func", VALUE_FUNCTIONS)
    def test_other_items(self, foreign_support_info: SupportInfoDump, value_func: Callable[[SupportInfoDump], float | None]):
        """Test ignoring items other than the configlayer."""
        assert value_func(foreign_support_info) is None
