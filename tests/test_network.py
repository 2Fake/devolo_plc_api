from unittest.mock import Mock, patch

import pytest
from zeroconf import ServiceStateChange, Zeroconf

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock

import devolo_plc_api.network as network
from devolo_plc_api.device import Device


class TestNetwork:

    @pytest.mark.asyncio
    async def test_async_discover_network(self, mocker):
        device = {
            "1234567890123456": Device(ip="123.123.123.123")
        }
        with patch("zeroconf.Zeroconf", new=Mock()), \
             patch("asyncio.sleep", new=AsyncMock()), \
             patch("devolo_plc_api.device.Device.async_connect", new=AsyncMock()):
            network._devices = device
            spy_connect = mocker.spy(Device, "async_connect")
            discovered = await network.async_discover_network()
            assert spy_connect.call_count == 1
            assert discovered == device

    def test_discover_network(self, mocker):
        device = {
            "1234567890123456": Device(ip="123.123.123.123")
        }
        with patch("zeroconf.ServiceBrowser", new=Mock()), \
             patch("time.sleep", new=Mock()), \
             patch("devolo_plc_api.device.Device.connect", new=Mock()):
            network._devices = device
            spy_connect = mocker.spy(Device, "connect")
            discovered = network.discover_network()
            assert spy_connect.call_count == 1
            assert discovered == device

    def test__add(self, mocker):
        service_info = {
            "properties": {
                "SN": "1234567890123456"
            },
            "address": "123.123.123.123",
        }
        with patch("zeroconf.Zeroconf.get_service_info", return_value="service_info"), \
             patch("devolo_plc_api.device.Device.info_from_service", return_value=service_info):
            network._add(Zeroconf(), "_dvl-deviceapi._tcp.local.", "_dvl-deviceapi._tcp.local.", ServiceStateChange.Added)
            assert "1234567890123456" in network._devices

    def test__add_no_device(self, mocker):
        with patch("zeroconf.Zeroconf.get_service_info", return_value=None):
            spy_info = mocker.spy(Device, "info_from_service")
            network._add(Zeroconf(), "_dvl-deviceapi._tcp.local.", "_dvl-deviceapi._tcp.local.", ServiceStateChange.Added)
            assert spy_info.call_count == 0

    def test__add_no_info(self, mocker):
        with patch("zeroconf.Zeroconf.get_service_info", return_value="service_info"), \
             patch("devolo_plc_api.device.Device.info_from_service", return_value=None):
            spy_device = mocker.spy(Device, "__init__")
            network._add(Zeroconf(), "_dvl-deviceapi._tcp.local.", "_dvl-deviceapi._tcp.local.", ServiceStateChange.Added)
            assert spy_device.call_count == 0
