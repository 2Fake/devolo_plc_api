"""Test communicating with a devolo device."""

from asyncio import AbstractEventLoop
from unittest.mock import AsyncMock, Mock, patch

import pytest
from syrupy.assertion import SnapshotAssertion
from zeroconf import ServiceStateChange

from devolo_plc_api.device import Device
from devolo_plc_api.exceptions import DeviceNotFound
from devolo_plc_api.plcnet_api import SERVICE_TYPE as PLCNETAPI

from . import DeviceType, TestData
from .mocks.zeroconf import MockAsyncServiceInfo


@pytest.mark.usefixtures("block_communication")
class TestDevice:
    """Test devolo_plc_api.device.Device class."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("service_browser")
    async def test_async_connect_plc(self, mock_device: Device, snapshot: SnapshotAssertion):
        """Test that connecting to a device collects information from the APIs."""
        await mock_device.async_connect()
        assert mock_device._connected
        assert mock_device.device
        assert mock_device.plcnet
        assert mock_device == snapshot
        await mock_device.async_disconnect()

        await mock_device.async_connect(session_instance=AsyncMock())
        assert mock_device._connected
        assert mock_device.device
        assert mock_device.plcnet
        assert mock_device == snapshot
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.REPEATER])
    @pytest.mark.usefixtures("service_browser")
    async def test_async_connect_repeater(self, mock_device: Device, snapshot: SnapshotAssertion):
        """Test that connecting to a device collects information from the APIs."""
        await mock_device.async_connect()
        assert mock_device._connected
        assert mock_device.device
        assert not mock_device.plcnet
        assert mock_device == snapshot
        await mock_device.async_disconnect()

    @pytest.mark.asyncio
    async def test_sync_connect_multicast(self, test_data: TestData):
        """Test that devices having trouble with unicast zeroconf are queried twice."""
        with patch("devolo_plc_api.device.Device._get_zeroconf_info") as get_zeroconf_info, pytest.raises(DeviceNotFound):
            device = Device(test_data.ip)
            await device.async_connect()
            assert device._multicast
            assert get_zeroconf_info.call_count == 2

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("service_browser")
    async def test_async_connect_not_found(self, mock_device: Device, sleep: AsyncMock):
        """Test that an exception is raised if both APIs are not available."""
        with pytest.raises(DeviceNotFound):
            await mock_device.async_connect()
            assert not mock_device._connected
            assert sleep.call_count == Device.MDNS_TIMEOUT

    def test_connect(self, mock_device: Device):
        """Test that the sync connect method just calls the async connect method."""
        with patch("devolo_plc_api.device.Device.async_connect", new=AsyncMock()) as ac:
            mock_device.connect()
            assert ac.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("service_browser")
    async def test_set_password(self, mock_device: Device):
        """Test setting a device password is also reflected in the APIs."""
        await mock_device.async_connect()
        assert mock_device.device
        assert mock_device.plcnet
        mock_device.password = "super_secret"
        assert mock_device.device.password == "super_secret"
        assert mock_device.plcnet.password == "super_secret"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("http_client", "service_browser")
    async def test_async_disconnect(self, mock_device: Device):
        """Test that disconnecting from a device cleans up Zeroconf and the HTTP client."""
        await mock_device.async_connect()
        await mock_device.async_disconnect()
        assert mock_device._zeroconf.async_close.call_count == 1  # type: ignore[attr-defined]
        assert mock_device._session.aclose.call_count == 1  # type: ignore[attr-defined]
        assert not mock_device._connected

        await mock_device.async_connect(session_instance=AsyncMock())
        await mock_device.async_disconnect()
        assert mock_device._zeroconf.async_close.call_count == 1  # type: ignore[attr-defined]
        assert mock_device._session.aclose.call_count == 0  # type: ignore[attr-defined]
        assert not mock_device._connected

    def test_disconnect(self, mock_device: Device, event_loop: AbstractEventLoop):
        """Test that the sync disconnect method just calls the async disconnect method."""
        with patch("devolo_plc_api.device.Device.async_disconnect", new=AsyncMock()) as ad:
            mock_device._loop = event_loop
            mock_device.disconnect()
            assert ad.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    @pytest.mark.usefixtures("service_browser")
    async def test_async_context_manager(self, test_data: TestData):
        """Test the async context manager."""
        async with Device(test_data.ip) as device:
            assert device._connected
        assert not device._connected

    @pytest.mark.usefixtures("service_browser")
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    def test_context_manager(self, test_data: TestData):
        """Test the sync context manager."""
        with Device(test_data.ip) as device:
            assert device._connected
        assert not device._connected

    @pytest.mark.asyncio
    async def test_state_change_removed(self, mock_device: Device):
        """Test that service information are not processed on state change to removed."""
        with (
            patch("devolo_plc_api.device.Device._retry_zeroconf_info"),
            patch("devolo_plc_api.device.Device._get_service_info") as gsi,
        ):
            mock_device._state_change(Mock(), PLCNETAPI, PLCNETAPI, ServiceStateChange.Removed)
            assert gsi.call_count == 0

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("service_browser", "sleep")
    @pytest.mark.parametrize("device_type", [DeviceType.PLC])
    async def test_get_service_info_alien(self, mock_info_from_service: Mock):
        """Test ignoring alien information discovered via mDNS."""
        with pytest.raises(DeviceNotFound):
            mock_device = Device(ip="192.0.2.2")
            await mock_device.async_connect()
            assert MockAsyncServiceInfo.async_request.call_count == 1
            assert mock_info_from_service.call_count == 0
