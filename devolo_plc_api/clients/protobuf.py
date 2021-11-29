from __future__ import annotations

import asyncio
import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable

from google.protobuf.json_format import MessageToDict
from httpx import (AsyncClient,
                   ConnectError,
                   ConnectTimeout,
                   DigestAuth,
                   HTTPStatusError,
                   ReadTimeout,
                   RemoteProtocolError,
                   Response)

from ..exceptions.device import DevicePasswordProtected, DeviceUnavailable

TIMEOUT = 10.0


class Protobuf(ABC):
    """
    Google Protobuf client.
    """

    @abstractmethod
    def __init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

        self.password: str

        self._ip: str
        self._path: str
        self._port: int
        self._session: AsyncClient
        self._user: str
        self._version: str

    def __getattr__(self, attr: str) -> Callable:
        """ Catch attempts to call methods synchronously. """

        def method(*args, **kwargs):
            return asyncio.run(getattr(self, async_method)(*args, **kwargs))

        async_method = f"async_{attr}"
        if hasattr(self.__class__, async_method):
            return method
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {attr}")

    @property
    def url(self) -> str:
        """ The base URL to query. """
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"

    async def _async_get(self, sub_url: str, timeout: float = TIMEOUT) -> Response:
        """ Query URL asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug("Getting from %s", url)

        async def get():
            response = await self._session.get(url, auth=DigestAuth(self._user, self.password), timeout=timeout)
            response.raise_for_status()
            return response

        try:
            return await get()
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                try:
                    self.password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
                    return await get()
                except HTTPStatusError:
                    raise DevicePasswordProtected("The used password is wrong.") from None
            raise e
        except (ConnectTimeout, ConnectError, ReadTimeout, RemoteProtocolError):
            raise DeviceUnavailable("The device is currenctly not available. Maybe on standby?") from None

    async def _async_post(self, sub_url: str, content: bytes, timeout: float = TIMEOUT) -> Response:
        """ Post data asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug("Posting to %s", url)

        async def post():
            response = await self._session.post(url,
                                                auth=DigestAuth(self._user,
                                                                self.password),
                                                content=content,
                                                timeout=timeout)
            response.raise_for_status()
            return response

        try:
            return await post()
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                try:
                    self.password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
                    return await post()
                except HTTPStatusError:
                    raise DevicePasswordProtected("The used password is wrong.") from None
            raise e
        except (ConnectTimeout, ConnectError, ReadTimeout, RemoteProtocolError):
            raise DeviceUnavailable("The device is currenctly not available. Maybe on standby?") from None

    @staticmethod
    def _message_to_dict(message) -> dict[str, Any]:
        """ Convert message to dict with certain settings. """
        return MessageToDict(message=message, including_default_value_fields=True, preserving_proto_field_name=True)
