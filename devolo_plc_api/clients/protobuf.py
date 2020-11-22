from abc import ABC, abstractmethod
from logging import Logger
from typing import Union

from google.protobuf.json_format import MessageToDict
from httpx import AsyncClient, Client, DigestAuth, Response

from ..exceptions.device import DevicePasswordProtected

TIMEOUT = 3.0


class Protobuf(ABC):
    """
    Google Protobuf client.
    """
    _logger: Logger

    @abstractmethod
    def __init__(self):
        self._ip: str
        self._password: str
        self._path: str
        self._port: int
        self._session: Union[AsyncClient, Client]
        self._user: str
        self._version: str


    @property
    def url(self) -> str:
        """ The base URL to query. """
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"


    @staticmethod
    def _message_to_dict(message) -> dict:
        """ Convert message to dict with certain settings. """
        return MessageToDict(message=message, including_default_value_fields=True, preserving_proto_field_name=True)


    async def _async_get(self, sub_url: str, timeout: float = TIMEOUT) -> Response:
        """ Query URL asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Getting from {url}")
        try:
            return await self._session.get(url,  # type: ignore
                                           auth=DigestAuth(self._user, self._password),
                                           timeout=timeout)
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None

    def _get(self, sub_url: str, timeout: float = TIMEOUT) -> Response:
        """ Query URL synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Getting from {url}")
        try:
            return self._session.get(url,  # type: ignore
                                     auth=DigestAuth(self._user, self._password),
                                     timeout=timeout)
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None

    async def _async_post(self, sub_url: str, content: bytes, timeout: float = TIMEOUT) -> Response:
        """ Post data asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Posting to {url}")
        try:
            return await self._session.post(url,  # type: ignore
                                            auth=DigestAuth(self._user, self._password),
                                            content=content,
                                            timeout=timeout)
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None

    def _post(self, sub_url: str, content: bytes, timeout: float = TIMEOUT) -> Response:
        """ Post data synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Posting to {url}")
        try:
            return self._session.post(url,  # type: ignore
                                      auth=DigestAuth(self._user, self._password),
                                      content=content,
                                      timeout=timeout)
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None
