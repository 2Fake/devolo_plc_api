"""Implementation of the devolo plcnet API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devolo_plc_api.clients import Protobuf

from .getnetworkoverview_pb2 import GetNetworkOverview
from .identifydevice_pb2 import IdentifyDeviceResponse, IdentifyDeviceStart, IdentifyDeviceStop
from .pairdevice_pb2 import PairDeviceResponse, PairDeviceStart
from .setuserdevicename_pb2 import SetUserDeviceName, SetUserDeviceNameResponse

if TYPE_CHECKING:
    from httpx import AsyncClient

    from devolo_plc_api.zeroconf import ZeroconfServiceInfo


class PlcNetApi(Protobuf):
    """
    Implementation of the devolo plcnet API.

    :param ip: IP address of the device to communicate with
    :param session: HTTP client session
    :param info: Information collected from the mDNS query
    """

    def __init__(self, ip: str, session: AsyncClient, info: ZeroconfServiceInfo) -> None:
        """Initialize the plcnet API."""
        super().__init__()

        self._ip = ip
        self._mac = info.properties["PlcMacAddress"]
        self._path = info.properties["Path"]
        self._port = info.port
        self._session = session
        self._user = "devolo"
        self._version = info.properties["Version"]

        self.password = ""

    async def async_get_network_overview(self) -> GetNetworkOverview.LogicalNetwork:
        """
        Get a PLC network overview.

        :return: Network overview
        """
        self._logger.debug("Getting network overview.")
        network_overview = GetNetworkOverview()
        response = await self._async_get("GetNetworkOverview")
        network_overview.ParseFromString(await response.aread())
        return network_overview.network

    async def async_identify_device_start(self) -> bool:
        """
        Make PLC LED of a device blink to identify it.

        :return: True, if identifying was successfully started, otherwise False
        """
        self._logger.debug("Starting LED blinking.")
        identify_device = IdentifyDeviceStart()
        identify_device.mac_address = self._mac
        query = await self._async_post("IdentifyDeviceStart", content=identify_device.SerializeToString())
        response = IdentifyDeviceResponse()
        response.ParseFromString(await query.aread())
        return response.result == response.SUCCESS

    async def async_identify_device_stop(self) -> bool:
        """
        Stop the PLC LED blinking.

        :return: True, if identifying was successfully stopped, otherwise False
        """
        self._logger.debug("Stopping LED blinking.")
        identify_device = IdentifyDeviceStop()
        identify_device.mac_address = self._mac
        query = await self._async_post("IdentifyDeviceStop", content=identify_device.SerializeToString())
        response = IdentifyDeviceResponse()
        response.ParseFromString(await query.aread())
        return response.result == response.SUCCESS

    async def async_pair_device(self) -> bool:
        """
        Start pairing mode.

        :return: True, if pairing was started successfully, otherwise False
        """
        self._logger.debug("Pairing.")
        pair_device = PairDeviceStart()
        pair_device.mac_address = self._mac
        query = await self._async_post("PairDeviceStart", content=pair_device.SerializeToString())
        response = PairDeviceResponse()
        response.ParseFromString(await query.aread())
        return response.result == response.SUCCESS

    async def async_set_user_device_name(self, name: str) -> bool:
        """
        Set device name.

        :param name: Name, the device shall have
        :return: True, if the device was successfully renamed, otherwise False
        """
        self._logger.debug("Setting device name.")
        set_user_name = SetUserDeviceName()
        set_user_name.mac_address = self._mac
        set_user_name.user_device_name = name
        query = await self._async_post("SetUserDeviceName", content=set_user_name.SerializeToString())
        response = SetUserDeviceNameResponse()
        response.ParseFromString(await query.aread())
        return response.result == response.SUCCESS
