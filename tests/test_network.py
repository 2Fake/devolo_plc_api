"""Test network discovery."""
from socket import inet_aton
from unittest.mock import Mock, patch

import pytest
from zeroconf import ServiceStateChange, Zeroconf

from devolo_plc_api import Device, network
from devolo_plc_api.device_api import SERVICE_TYPE
from devolo_plc_api.zeroconf import ZeroconfServiceInfo

from . import TestData
from .mocks.mock_zeroconf import MockServiceBrowser


class TestNetwork:
    """Test devolo_plc_api.network functions."""

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("block_communication")
    async def test_async_discover_network(self, test_data: TestData, mock_info_from_service: Mock):
        """Test discovering the network asynchronously."""
        serial_number = test_data.device_info[SERVICE_TYPE].properties["SN"]
        mock_info_from_service.return_value = ZeroconfServiceInfo(
            address=inet_aton(test_data.ip), properties=test_data.device_info[SERVICE_TYPE].properties
        )
        discovered = await network.async_discover_network()
        assert serial_number in discovered
        assert isinstance(discovered[serial_number], Device)

    @pytest.mark.usefixtures("block_communication")
    def test_discover_network(self, test_data: TestData, mock_info_from_service: Mock):
        """Test discovering the network synchronously."""
        serial_number = test_data.device_info[SERVICE_TYPE].properties["SN"]
        mock_info_from_service.return_value = ZeroconfServiceInfo(
            address=inet_aton(test_data.ip), properties=test_data.device_info[SERVICE_TYPE].properties
        )
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
        ):
            discovered = network.discover_network()
            assert not discovered

    @pytest.mark.usefixtures("block_communication")
    @pytest.mark.parametrize("mt", ["2600", "2601"])
    def test_hcu(self, test_data: TestData, mt: str, mock_info_from_service: Mock):
        """Test ignoring Home Control Central Units."""
        mock_info_from_service.return_value = ZeroconfServiceInfo(address=test_data.ip.encode(), properties={"MT": mt})
        discovered = network.discover_network()
        assert not discovered
