"""Test network discovery."""
from unittest.mock import patch

import pytest
from zeroconf import ServiceStateChange, Zeroconf

from devolo_plc_api import Device, network
from devolo_plc_api.device_api import SERVICE_TYPE

from . import TestData
from .mocks.mock_zeroconf import MockServiceBrowser


class TestNetwork:
    """Test devolo_plc_api.network functions."""

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("block_communication")
    async def test_async_discover_network(self, test_data: TestData):
        """Test discovering the network asynchronously."""
        serial_number = test_data.device_info[SERVICE_TYPE]["properties"]["SN"]
        with patch("devolo_plc_api.network.ServiceBrowser", MockServiceBrowser), patch(
            "devolo_plc_api.device.Device.info_from_service",
            return_value={"address": test_data.ip, "properties": test_data.device_info[SERVICE_TYPE]["properties"]},
        ), patch("asyncio.sleep"):
            discovered = await network.async_discover_network()
            assert serial_number in discovered
            assert isinstance(discovered[serial_number], Device)

    @pytest.mark.usefixtures("block_communication")
    def test_discover_network(self, test_data: TestData):
        """Test discovering the network synchronously."""
        serial_number = test_data.device_info[SERVICE_TYPE]["properties"]["SN"]
        with patch("devolo_plc_api.network.ServiceBrowser", MockServiceBrowser), patch(
            "devolo_plc_api.device.Device.info_from_service",
            return_value={"address": test_data.ip, "properties": test_data.device_info[SERVICE_TYPE]["properties"]},
        ), patch("time.sleep"):
            discovered = network.discover_network()
            assert serial_number in discovered
            assert isinstance(discovered[serial_number], Device)

    # pylint: disable=protected-access
    def test_add_wrong_state(self):
        """Test early return on wrong state changes."""
        with patch("devolo_plc_api.network.Zeroconf.get_service_info") as gsi:
            network._add({}, Zeroconf(), SERVICE_TYPE, SERVICE_TYPE, ServiceStateChange.Removed)
            assert gsi.call_count == 0

    def test_no_devices(self):
        """Test discovery with no devices."""
        with patch("devolo_plc_api.network.ServiceBrowser", MockServiceBrowser), patch(
            "devolo_plc_api.network.Zeroconf.get_service_info", return_value=None
        ), patch("time.sleep"):
            discovered = network.discover_network()
            assert not discovered

    @pytest.mark.usefixtures("block_communication")
    def test_hcu(self, test_data: TestData):
        """Test ignoring Home Control Central Units."""
        with patch("devolo_plc_api.network.ServiceBrowser", MockServiceBrowser), patch(
            "devolo_plc_api.device.Device.info_from_service",
            return_value={"address": test_data.ip, "properties": {"MT": "2600"}},
        ), patch("time.sleep"):
            discovered = network.discover_network()
            assert not discovered

        with patch("devolo_plc_api.network.ServiceBrowser", MockServiceBrowser), patch(
            "devolo_plc_api.device.Device.info_from_service",
            return_value={"address": test_data.ip, "properties": {"MT": "2601"}},
        ), patch("time.sleep"):
            discovered = network.discover_network()
            assert not discovered
