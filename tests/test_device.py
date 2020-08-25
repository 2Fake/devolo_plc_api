from datetime import date
from unittest.mock import patch

import pytest
from asynctest import CoroutineMock

from devolo_plc_api.device_api.deviceapi import DeviceApi
from devolo_plc_api.plcnet_api.plcnetapi import PlcNetApi


class TestDevice:
    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_device_api")
    async def test___get_device_info(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_zeroconf_info", new=CoroutineMock()):
            device_info = self.device_info['_dvl-deviceapi._tcp.local.']
            await mock_device._get_device_info()

            assert mock_device.firmware_date == date.fromisoformat(device_info['FirmwareDate'])
            assert mock_device.firmware_version == device_info['FirmwareVersion']
            assert mock_device.serial_number == device_info['SN']
            assert mock_device.mt_number == device_info['MT']
            assert mock_device.product == device_info['Product']
            assert type(mock_device.device) == DeviceApi

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("mock_plcnet_api")
    async def test___get_plcnet_info(self, mock_device):
        with patch("devolo_plc_api.device.Device._get_zeroconf_info", new=CoroutineMock()):
            device_info = self.device_info['_dvl-plcnetapi._tcp.local.']
            await mock_device._get_plcnet_info()

            assert mock_device.mac == device_info['PlcMacAddress']
            assert mock_device.technology == device_info['PlcTechnology']
            assert type(mock_device.plcnet) == PlcNetApi
