from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from google.protobuf.json_format import MessageToDict
from httpx import AsyncClient, Response

from devolo_plc_api.device_api.deviceapi import DeviceApi
from devolo_plc_api.device_api.devolo_idl_proto_deviceapi_ledsettings_pb2 import LedSettingsGet


class TestDeviceApi:

    @pytest.mark.asyncio
    async def test_async_get_led_setting(self, request):
        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=b"")):
            device_api = DeviceApi(request.cls.ip,
                                   AsyncClient(),
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path'],
                                   request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version'],
                                   "led",
                                   "password")
            led_setting = await device_api.async_get_led_setting()

        assert led_setting == MessageToDict(LedSettingsGet(),
                                            including_default_value_fields=True,
                                            preserving_proto_field_name=True)
