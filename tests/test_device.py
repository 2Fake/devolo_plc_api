import pytest

from devolo_plc_api.device import Device


class TestDevice:
    @pytest.mark.usefixtures("mock_zeroconf")
    @pytest.mark.usefixtures("mock_device_api")
    @pytest.mark.usefixtures("mock_plcnet_api")
    def test___get_device_info(self):
        device = Device(ip="192.168.0.10", session="")
        device._get_device_info()
        assert device.serial_number == "1234567890123456"
