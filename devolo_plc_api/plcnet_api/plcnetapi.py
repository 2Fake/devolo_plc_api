"""Implementation of the devolo plcnet API."""
from __future__ import annotations

from typing import Any

from httpx import AsyncClient

from ..clients.protobuf import Protobuf
from . import getnetworkoverview_pb2, identifydevice_pb2, pairdevice_pb2, setuserdevicename_pb2


# Issue: https://github.com/PyCQA/pylint/issues/4987
class PlcNetApi(Protobuf):
    """
    Implementation of the devolo plcnet API.

    :param ip: IP address of the device to communicate with
    :param session: HTTP client session
    :param info: Information collected from the mDNS query
    """

    def __init__(self, ip: str, session: AsyncClient, info: dict[str, Any]) -> None:
        super().__init__()

        self._ip = ip
        self._mac = info["properties"]["PlcMacAddress"]
        self._path = info["properties"]["Path"]
        self._port = info["port"]
        self._session = session
        self._user = ""  # PLC API is not password protected.
        self._version = info["properties"]["Version"]

        self.password = ""  # PLC API is not password protected.

    async def async_get_network_overview(self) -> dict[str, dict]:
        """
        Get a PLC network overview.

        :return: Network overview
        """
        self._logger.debug("Getting network overview.")
        network_overview = getnetworkoverview_pb2.GetNetworkOverview()
        response = await self._async_get("GetNetworkOverview")
        network_overview.ParseFromString(await response.aread())
        return self._message_to_dict(network_overview)

    async def async_identify_device_start(self) -> bool:
        """
        Make PLC LED of a device blink to identify it.

        :return: True, if identifying was successfully started, otherwise False
        """
        self._logger.debug("Starting LED blinking.")
        identify_device = identifydevice_pb2.IdentifyDeviceStart()
        identify_device.mac_address = self._mac
        query = await self._async_post("IdentifyDeviceStart", content=identify_device.SerializeToString())
        response = identifydevice_pb2.IdentifyDeviceResponse()
        response.FromString(await query.aread())
        return response.result == response.SUCCESS  # pylint: disable=no-member

    async def async_identify_device_stop(self) -> bool:
        """
        Stop the PLC LED blinking.

        :return: True, if identifying was successfully stopped, otherwise False
        """
        self._logger.debug("Stopping LED blinking.")
        identify_device = identifydevice_pb2.IdentifyDeviceStop()
        identify_device.mac_address = self._mac
        query = await self._async_post("IdentifyDeviceStop", content=identify_device.SerializeToString())
        response = identifydevice_pb2.IdentifyDeviceResponse()
        response.FromString(await query.aread())
        return response.result == response.SUCCESS  # pylint: disable=no-member

    async def async_pair_device(self) -> bool:
        """
        Start pairing mode.

        :return: True, if pairing was started successfully, otherwise False
        """
        self._logger.debug("Pairing.")
        pair_device = pairdevice_pb2.PairDeviceStart()
        pair_device.mac_address = self._mac
        query = await self._async_post("PairDeviceStart", content=pair_device.SerializeToString())
        response = pairdevice_pb2.PairDeviceResponse()
        response.FromString(await query.aread())
        return response.result == response.SUCCESS  # pylint: disable=no-member

    async def async_set_user_device_name(self, name: str) -> bool:
        """
        Set device name.

        :param name: Name, the device shall have
        :return: True, if the device was successfully renamed, otherwise False
        """
        self._logger.debug("Setting device name.")
        set_user_name = setuserdevicename_pb2.SetUserDeviceName()
        set_user_name.mac_address = self._mac
        set_user_name.user_device_name = name
        query = await self._async_post("SetUserDeviceName", content=set_user_name.SerializeToString())
        response = setuserdevicename_pb2.SetUserDeviceNameResponse()
        response.FromString(await query.aread())
        return response.result == response.SUCCESS  # pylint: disable=no-member
