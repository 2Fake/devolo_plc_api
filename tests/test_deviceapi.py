from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from httpx import AsyncClient, Client, Response

from devolo_plc_api.device_api.deviceapi import DeviceApi


class TestDeviceApi:

    @pytest.mark.asyncio
    async def test_async_get_led_setting(self, request):
        ip = request.cls.ip
        session = AsyncClient()
        path = request.cls.device_info['_dvl-deviceapi._tcp.local.']['Path']
        version = request.cls.device_info['_dvl-deviceapi._tcp.local.']['Version']
        features = "led"
        password = "password"

        with patch("devolo_plc_api.clients.protobuf.Protobuf._async_get", new=CoroutineMock(return_value=Response)), \
             patch("httpx.Response.aread", new=CoroutineMock(return_value=b"")):
            device_api = DeviceApi(ip, session, path, version, features, password)
            led_setting = await device_api.async_get_led_setting()

        assert led_setting['state'] == "LED_ON"
