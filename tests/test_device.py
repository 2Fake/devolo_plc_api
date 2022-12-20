"""Test communicating with a devolo device."""
from datetime import date
from unittest.mock import AsyncMock, Mock, patch

import pytest
from zeroconf import ServiceStateChange

from devolo_plc_api.device import EMPTY_INFO, Device
from devolo_plc_api.device_api import SERVICE_TYPE as DEVICEAPI
from devolo_plc_api.device_api import DeviceApi
from devolo_plc_api.exceptions.device import DeviceNotFound
from devolo_plc_api.plcnet_api import DEVICES_WITHOUT_PLCNET
from devolo_plc_api.plcnet_api import SERVICE_TYPE as PLCNETAPI
from devolo_plc_api.plcnet_api import PlcNetApi
from tests.mocks.mock_zeroconf import MockServiceBrowser

from . import TestData
from .mocks.mock_device import state_change
from .stubs.zeroconf import StubAsyncServiceInfo


@pytest.mark.usefixtures("block_communication")
class TestDevice:
    """Test devolo_plc_api.device.Device class."""

    @pytest.mark.parametrize("feature", [""])
    def test_set_password(self, mock_device: Device, device_api: DeviceApi):
        """Test setting a device password is also reflected in the device API."""
        mock_device.device = device_api
        mock_device.password = "super_secret"
        assert mock_device.device.password == "super_secret"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", [""])
    async def test_async_connect(self, mock_device: Device, device_api: DeviceApi, plcnet_api: PlcNetApi):
        """Test that connecting to a device calls methos to collect information from the APIs."""
        with patch("devolo_plc_api.device.Device._get_device_info") as gdi, patch(
            "devolo_plc_api.device.Device._get_plcnet_info"
        ) as gpi:
            mock_device.device = device_api
            mock_device.plcnet = plcnet_api
            await mock_device.async_connect()
            assert gdi.call_count == 1
            assert gpi.call_count == 1
            assert getattr(mock_device, "_connected")

            await mock_device.async_connect(session_instance=AsyncMock())
            assert gdi.call_count == 2
            assert gpi.call_count == 2
            assert getattr(mock_device, "_connected")

    @pytest.mark.asyncio
    async def test_async_connect_not_found(self, mock_device: Device):
        """Test that an exception is raised if both APIs are not available."""
        with patch("devolo_plc_api.device.Device._get_device_info"), patch(
            "devolo_plc_api.device.Device._get_plcnet_info"
        ), pytest.raises(DeviceNotFound):
            await mock_device.async_connect()
            assert not getattr(mock_device, "_connected")

    def test_connect(self, mock_device: Device):
        """Test that the sync connect method just calls the async connect method."""
        with patch("devolo_plc_api.device.Device.async_connect", new=AsyncMock()) as ac:
            mock_device.connect()
            assert ac.call_count == 1

    @pytest.mark.asyncio
    # pylint: disable=protected-access
    async def test_async_disconnect(self, mock_device: Device):
        """Test that disconnecting from a device cleans up Zeroconf and the HTTP client."""
        await mock_device.async_connect()
        await mock_device.async_disconnect()
        assert mock_device._zeroconf.async_close.call_count == 1  # type: ignore
        assert mock_device._session.aclose.call_count == 1  # type: ignore
        assert not getattr(mock_device, "_connected")

        await mock_device.async_connect(session_instance=AsyncMock())
        await mock_device.async_disconnect()
        assert mock_device._zeroconf.async_close.call_count == 1  # type: ignore
        assert mock_device._session.aclose.call_count == 0  # type: ignore
        assert not getattr(mock_device, "_connected")

    def test_disconnect(self, mock_device: Device):
        """Test that the sync disconnect method just calls the async disconnect method."""
        with patch("devolo_plc_api.device.Device.async_disconnect", new=AsyncMock()) as ad:
            mock_device.disconnect()
            assert ad.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_service_browser")
    async def test_async_context_manager(self, test_data: TestData):
        """Test the async context manager."""
        with patch("devolo_plc_api.device.Device._state_change", state_change):
            async with Device(test_data.ip) as device:
                assert getattr(device, "_connected")
            assert not getattr(device, "_connected")

    @pytest.mark.usefixtures("mock_service_browser")
    def test_context_manager(self, test_data: TestData):
        """Test the sync context manager."""
        with patch("devolo_plc_api.device.Device._state_change", state_change):
            with Device(test_data.ip) as device:
                assert getattr(device, "_connected")
            assert not getattr(device, "_connected")

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_api")
    async def test__get_device_info(self, mock_device: Device, test_data: TestData):
        """Test that information from the device API are filled in."""
        with patch("devolo_plc_api.device.Device._get_zeroconf_info"):
            device_info = test_data.device_info[DEVICEAPI]
            mock_device.password = "super_secret"
            await mock_device.async_connect()
            assert mock_device.firmware_date == date.fromisoformat(device_info["properties"]["FirmwareDate"])
            assert mock_device.firmware_version == device_info["properties"]["FirmwareVersion"]
            assert mock_device.serial_number == device_info["properties"]["SN"]
            assert mock_device.mt_number == device_info["properties"]["MT"]
            assert mock_device.product == device_info["properties"]["Product"]
            assert isinstance(mock_device.device, DeviceApi)
            assert mock_device.device.password == mock_device.password

    @pytest.mark.asyncio
    async def test__get_device_info_multicast(self, test_data: TestData):
        """Test that devices having trouble with unicast zeroconf are queried twice."""
        with patch("devolo_plc_api.device.Device._get_zeroconf_info") as gzi, pytest.raises(DeviceNotFound):
            device = Device(test_data.ip)
            await device.async_connect()
            assert getattr(device, "_multicast")
            assert gzi.call_count == 2

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_plcnet_api")
    async def test__get_plcnet_info(self, mock_device: Device, test_data: TestData):
        """Test that information from the plcnet API are filled in."""
        with patch("devolo_plc_api.device.Device._get_zeroconf_info"):
            device_info = test_data.device_info[PLCNETAPI]
            await mock_device.async_connect()
            assert mock_device.mac == device_info["properties"]["PlcMacAddress"]
            assert mock_device.technology == device_info["properties"]["PlcTechnology"]
            assert isinstance(mock_device.plcnet, PlcNetApi)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("feature", [""])
    async def test__not_get_plcnet_info(self, mock_device: Device, device_api: DeviceApi):
        """Test that devices know to not have a plcnet API don't query it."""
        mock_device.mt_number = DEVICES_WITHOUT_PLCNET[0]
        with patch("devolo_plc_api.device.Device._get_zeroconf_info") as gzi, patch(
            "devolo_plc_api.device.Device._get_device_info"
        ):
            mock_device.device = device_api
            await mock_device.async_connect()
            assert gzi.call_count == 0
            assert not mock_device.plcnet

    @pytest.mark.asyncio
    async def test__get_plcnet_info_multicast(self, test_data: TestData):
        """Test that devices having trouble with unicast zeroconf are queried twice."""
        with patch("devolo_plc_api.device.Device._get_zeroconf_info") as gzi, pytest.raises(DeviceNotFound):
            device = Device(test_data.ip)
            await device.async_connect()
            assert getattr(device, "_multicast")
            assert gzi.call_count == 2

    @pytest.mark.asyncio
    # pylint: disable=protected-access
    async def test__get_zeroconf_info_timeout(self, mock_device: Device):
        """Test that the mDNS service browser times out after 3 seconds."""
        mock_device._info["_http._tcp.local."] = EMPTY_INFO
        await mock_device.async_connect()
        with patch("devolo_plc_api.device.AsyncServiceBrowser._async_start"), patch(
            "devolo_plc_api.device.AsyncServiceBrowser._async_cancel"
        ), patch("asyncio.sleep") as sleep:
            await mock_device._get_zeroconf_info("_http._tcp.local.")
            assert sleep.call_count == 300

    @pytest.mark.asyncio
    async def test__get_zeroconf_info_device_info_exists(self, mock_device: Device, mock_service_browser: MockServiceBrowser):
        """Test early return if information already exist."""
        await mock_device.async_connect()
        assert mock_service_browser.async_cancel.call_count == 0

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_service_browser")
    async def test__state_change_no_service_info(self, test_data: TestData):
        """Test that waiting for mDNS responses continues, if no service info were received."""
        with patch("devolo_plc_api.device.Device.info_from_service") as ifs, patch(
            "devolo_plc_api.device.AsyncServiceInfo.async_request"
        ), patch("asyncio.sleep"):
            mock_device = Device(ip=test_data.ip, plcnetapi=None, deviceapi=test_data.device_info[DEVICEAPI])
            await mock_device.async_connect()
            assert ifs.call_count == 0

    @pytest.mark.asyncio
    # pylint: disable=protected-access
    async def test__state_change_removed(self, mock_device: Device):
        """Test that service information are not processed on state change to removed."""
        with patch("devolo_plc_api.device.Device._retry_zeroconf_info"), patch(
            "devolo_plc_api.device.Device._get_service_info"
        ) as gsi:
            mock_device._state_change(Mock(), PLCNETAPI, PLCNETAPI, ServiceStateChange.Removed)
            assert gsi.call_count == 0

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_service_browser")
    async def test__get_service_info(self, test_data: TestData):
        """Test storing of information discovered via mDNS."""
        with patch("devolo_plc_api.device.AsyncServiceInfo", StubAsyncServiceInfo), patch(
            "devolo_plc_api.device.PlcNetApi"
        ), patch("devolo_plc_api.device.AsyncServiceInfo.async_request") as ar:
            mock_device = Device(ip=test_data.ip, plcnetapi=None, deviceapi=test_data.device_info[DEVICEAPI])
            await mock_device.async_connect()
            assert ar.call_count == 2
            assert mock_device.mac == test_data.device_info[PLCNETAPI]["properties"]["PlcMacAddress"]

    def test_info_from_service_no_address(self, mock_device: Device):
        """Test ignoring information received for an other address."""
        service_info = Mock()
        service_info.addresses = None
        assert mock_device.info_from_service(service_info) == {}
