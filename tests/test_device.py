import asyncio
from datetime import date
from unittest.mock import Mock, patch

import pytest
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

from devolo_plc_api.device import EMPTY_INFO
from devolo_plc_api.device_api.deviceapi import DeviceApi
from devolo_plc_api.exceptions.device import DeviceNotFound
from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi

from .mocks.mock_devices import state_change


class TestDevice:

    @pytest.mark.parametrize("feature", [""])
    def test_set_password(self, mock_device, device_api):
        mock_device.device = device_api
        mock_device.password = "super_secret"
        assert mock_device.device.password == "super_secret"

    @pytest.mark.asyncio
    async def test_async_connect(self, mocker, mock_device):
        with patch("devolo_plc_api.device.Device._get_device_info", new=AsyncMock()), \
             patch("devolo_plc_api.device.Device._get_plcnet_info", new=AsyncMock()):
            spy_device_info = mocker.spy(mock_device, "_get_device_info")
            spy_plcnet_info = mocker.spy(mock_device, "_get_plcnet_info")
            mock_device.device = object
            mock_device.plcnet = object
            await mock_device.async_connect()
            assert spy_device_info.call_count == 1
            assert spy_plcnet_info.call_count == 1
            assert mock_device._connected

    @pytest.mark.asyncio
    async def test_async_connect_not_found(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_device_info", new=AsyncMock()), \
             patch("devolo_plc_api.device.Device._get_plcnet_info", new=AsyncMock()), \
             pytest.raises(DeviceNotFound):
            await mock_device.async_connect()
        assert not mock_device._connected

    def test_connect(self, mocker, mock_device):
        with patch("devolo_plc_api.device.Device.async_connect", new=AsyncMock()):
            spy_connect = mocker.spy(mock_device, "async_connect")
            mock_device.connect()
            assert spy_connect.call_count == 1

    @pytest.mark.asyncio
    async def test_async_disconnect(self, mocker, mock_device):
        spy_zeroconf = mocker.spy(mock_device._zeroconf, "close")
        spy_session = mocker.spy(mock_device._session, "aclose")
        await mock_device.async_disconnect()
        assert spy_zeroconf.call_count == 1
        assert spy_session.call_count == 1
        assert not mock_device._connected

    def test_disconnect(self, mocker, mock_device):
        with patch("devolo_plc_api.device.Device.async_disconnect", new=AsyncMock()):
            spy_connect = mocker.spy(mock_device, "async_disconnect")
            mock_device.disconnect()
            assert spy_connect.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_api")
    async def test__get_device_info(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_zeroconf_info", new=AsyncMock()):
            device_info = self.device_info['_dvl-deviceapi._tcp.local.']
            await mock_device._get_device_info()
            assert mock_device.firmware_date == date.fromisoformat(device_info["properties"]["FirmwareDate"])
            assert mock_device.firmware_version == device_info["properties"]["FirmwareVersion"]
            assert mock_device.serial_number == device_info["properties"]["SN"]
            assert mock_device.mt_number == device_info["properties"]["MT"]
            assert mock_device.product == device_info["properties"]["Product"]
            assert type(mock_device.device) == DeviceApi

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_api")
    async def test__get_device_info_timeout(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_zeroconf_info", new=Mock()), \
             patch("asyncio.wait_for", new=AsyncMock(side_effect=asyncio.TimeoutError())):
            await mock_device._get_device_info()
            assert mock_device.device is None

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_plcnet_api")
    async def test__get_plcnet_info(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_zeroconf_info", new=AsyncMock()):
            device_info = self.device_info["_dvl-plcnetapi._tcp.local."]
            await mock_device._get_plcnet_info()
            assert mock_device.mac == device_info["properties"]["PlcMacAddress"]
            assert mock_device.technology == device_info["properties"]["PlcTechnology"]
            assert type(mock_device.plcnet) == PlcNetApi

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_plcnet_api")
    async def test__get_plcnet_info_timeout(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_zeroconf_info", new=Mock()), \
             patch("asyncio.wait_for", new=AsyncMock(side_effect=asyncio.TimeoutError())):
            await mock_device._get_plcnet_info()
            assert mock_device.plcnet is None

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_service_browser")
    async def test__get_zeroconf_info(self, mocker, mock_device):
        with patch("devolo_plc_api.device.Device._state_change", state_change):
            mock_device._info["_dvl-plcnetapi._tcp.local."] = EMPTY_INFO
            spy_cancel = mocker.spy(ServiceBrowser, "cancel")
            await mock_device._get_zeroconf_info("_dvl-plcnetapi._tcp.local.")
            assert spy_cancel.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_service_browser")
    async def test__get_zeroconf_info_device_info_exists(self, mocker, mock_device):
        spy_cancel = mocker.spy(ServiceBrowser, "cancel")
        await mock_device._get_zeroconf_info("_dvl-plcnetapi._tcp.local.")
        assert spy_cancel.call_count == 0

    def test__state_change_no_service_info(self, mocker, mock_device):
        with patch("zeroconf.Zeroconf.get_service_info", return_value=None):
            service_type = "_dvl-plcnetapi._tcp.local."
            spy_service_info = mocker.spy(mock_device, "info_from_service")
            mock_device._state_change(Zeroconf(), service_type, service_type, ServiceStateChange.Added)
            assert spy_service_info.call_count == 0

    def test__state_change_added(self, mock_device, mock_zeroconf):
        service_type = "_dvl-plcnetapi._tcp.local."
        mock_device._state_change(mock_zeroconf, service_type, service_type, ServiceStateChange.Added)
        assert mock_device._info[service_type]["properties"]["new"] == "value"

    def test__state_change_removed(self, mock_device, mock_zeroconf):
        service_type = "_dvl-plcnetapi._tcp.local."
        mock_device._state_change(mock_zeroconf, service_type, service_type, ServiceStateChange.Removed)
        assert "new" not in mock_device._info[service_type]

    def test_info_from_service_no_address(self, mock_device):
        service_info = Mock()
        service_info.addresses = None
        assert mock_device.info_from_service(service_info) is None
