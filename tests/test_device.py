from unittest.mock import patch
from datetime import date
import pytest
from asynctest import CoroutineMock
from devolo_plc_api.device_api.deviceapi import DeviceApi


class TestDevice:
    @pytest.mark.usefixtures("mock_device_api")
    @pytest.mark.asyncio
    async def test___get_device_info(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_zeroconf_info", new=CoroutineMock()):
            await mock_device._get_device_info()
            assert mock_device.firmware_date == date.fromisoformat(self.device_info["_dvl-deviceapi._tcp.local."]["FirmwareDate"])
            assert mock_device.firmware_version == self.device_info["_dvl-deviceapi._tcp.local."]["FirmwareVersion"]
            assert mock_device.serial_number == self.device_info["_dvl-deviceapi._tcp.local."]["SN"]
            assert mock_device.mt_number == self.device_info["_dvl-deviceapi._tcp.local."]["MT"]
            assert mock_device.product == self.device_info["_dvl-deviceapi._tcp.local."]["Product"]
            assert type(mock_device.device) == DeviceApi

