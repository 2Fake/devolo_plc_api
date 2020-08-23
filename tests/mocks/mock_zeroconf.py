def _get_zeroconf_info(self, service_type):
    if service_type == "_dvl-deviceapi._tcp.local.":
        self._info = {
            "FirmwareDate": "2020-06-29",
            "FirmwareVersion": "5.5.1",
            "SN": "1234567890123456",
            "MT": "2730",
            "Product": "dLAN pro 1200+ WiFi ac",
            "Path": "/",
            "Version": "v0",
            "Features": "wifi1"
        }
    elif service_type == "_dvl-plcnetapi._tcp.local.":
        self._info = {
            "PlcMacAddress": "000000000000",
            "PlcTechnology": "hpav",
            "Path": "/",
            "Version": "v0"
        }
