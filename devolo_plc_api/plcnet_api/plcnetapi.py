from typing import Dict

from httpx import AsyncClient

from ..clients.protobuf import Protobuf
from . import (devolo_idl_proto_plcnetapi_getnetworkoverview_pb2,
               devolo_idl_proto_plcnetapi_identifydevice_pb2,
               devolo_idl_proto_plcnetapi_setuserdevicename_pb2)


class PlcNetApi(Protobuf):
    """
    Implementation of the devolo plcnet API.

    :param ip: IP address of the device to communicate with
    :param session: HTTP client session
    :param info: Information collected from the mDNS query
    """

    def __init__(self, ip: str, session: AsyncClient, info: Dict):
        super().__init__()

        self._ip = ip
        self._mac = info["properties"]["PlcMacAddress"]
        self._path = info["properties"]["Path"]
        self._port = info["port"]
        self._session = session
        self._user = ""  # PLC API is not password protected.
        self._version = info["properties"]["Version"]

        self.password = ""  # PLC API is not password protected.

    async def async_get_network_overview(self) -> dict:
        """
        Get a PLC network overview.

        :return: Network overview
        """
        self._logger.debug("Getting network overview.")
        network_overview = devolo_idl_proto_plcnetapi_getnetworkoverview_pb2.GetNetworkOverview()
        response = await self._async_get("GetNetworkOverview")
        network_overview.ParseFromString(await response.aread())
        return self._message_to_dict(network_overview)

    async def async_identify_device_start(self) -> bool:
        """
        Make PLC LED of a device blick to identify it.

        :return: True, if identifying was successfully started, otherwise False
        """
        self._logger.debug("Starting LED blinking.")
        identify_device = devolo_idl_proto_plcnetapi_identifydevice_pb2.IdentifyDeviceStart()
        identify_device.mac_address = self._mac
        query = await self._async_post("IdentifyDeviceStart", content=identify_device.SerializeToString())
        response = devolo_idl_proto_plcnetapi_identifydevice_pb2.IdentifyDeviceResponse()
        response.FromString(await query.aread())  # pylint: disable=no-member
        return bool(not response.result)  # pylint: disable=no-member

    async def async_identify_device_stop(self) -> bool:
        """
        Stop the PLC LED blicking.

        :return: True, if identifying was successfully stopped, otherwise False
        """
        self._logger.debug("Stopping LED blinking.")
        identify_device = devolo_idl_proto_plcnetapi_identifydevice_pb2.IdentifyDeviceStop()
        identify_device.mac_address = self._mac
        query = await self._async_post("IdentifyDeviceStop", content=identify_device.SerializeToString())
        response = devolo_idl_proto_plcnetapi_identifydevice_pb2.IdentifyDeviceResponse()
        response.FromString(await query.aread())  # pylint: disable=no-member
        return bool(not response.result)  # pylint: disable=no-member

    async def async_set_user_device_name(self, name) -> bool:
        """
        Set device name.

        :param name: Name, the device shall have
        :return: True, if the device was successfully renamed, otherwise False
        """
        self._logger.debug("Setting device name.")
        set_user_name = devolo_idl_proto_plcnetapi_setuserdevicename_pb2.SetUserDeviceName()
        set_user_name.mac_address = self._mac
        set_user_name.user_device_name = name
        query = await self._async_post("SetUserDeviceName", content=set_user_name.SerializeToString(), timeout=10.0)
        response = devolo_idl_proto_plcnetapi_setuserdevicename_pb2.SetUserDeviceNameResponse()
        response.FromString(await query.aread())  # pylint: disable=no-member
        return bool(not response.result)  # pylint: disable=no-member
