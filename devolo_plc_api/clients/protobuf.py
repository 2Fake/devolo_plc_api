"""Google Protobuf client."""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from hashlib import sha256
from http import HTTPStatus
from typing import Any, Callable

from httpx import (
    AsyncClient,
    ConnectError,
    ConnectTimeout,
    DigestAuth,
    HTTPStatusError,
    ReadTimeout,
    RemoteProtocolError,
    Response,
)
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from devolo_plc_api.exceptions import DevicePasswordProtected, DeviceUnavailable

TIMEOUT = 10.0


class Protobuf(ABC):
    """Google Protobuf client as ground work."""

    @abstractmethod
    def __init__(self) -> None:
        """Initialize the client."""
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

        self.password: str

        self._ip: str
        self._path: str
        self._port: int
        self._session: AsyncClient
        self._user: str
        self._version: str

    def __getattr__(self, attr: str) -> Callable[..., Any]:
        """Catch attempts to call methods synchronously."""

        def method(*args: Any, **kwargs: Any) -> Any:
            return asyncio.run(getattr(self, async_method)(*args, **kwargs))

        async_method = f"async_{attr}"
        if hasattr(self.__class__, async_method):
            return method
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {attr}")  # noqa: EM102, TRY003

    @property
    def url(self) -> str:
        """The base URL to query."""
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"

    async def _async_get(self, sub_url: str, timeout: float = TIMEOUT) -> Response:
        """Query URL asynchronously."""
        url = f"{self.url}{sub_url}"
        self._logger.debug("Getting from %s", url)
        return await self._async_request("GET", url, None, timeout)

    async def _async_post(self, sub_url: str, content: bytes, timeout: float = TIMEOUT) -> Response:
        """Post data asynchronously."""
        url = f"{self.url}{sub_url}"
        self._logger.debug("Posting to %s", url)
        return await self._async_request("POST", url, content, timeout)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=5),
        retry=retry_if_exception_type(DeviceUnavailable),
        reraise=True,
        before_sleep=before_sleep_log(logging.getLogger("devolo_plc_api.clients.protobuf.Protobuf"), logging.DEBUG),
    )
    async def _async_request(self, method: str, url: str, content: bytes | None, timeout: float = TIMEOUT) -> Response:
        """Request data asynchronously."""
        try:
            response = await self._session.request(
                method,
                url,
                auth=DigestAuth(self._user, self.password),
                content=content,
                timeout=timeout,
            )
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                self.password = sha256(self.password.encode("utf-8")).hexdigest()
                response = await self._session.request(
                    method,
                    url,
                    auth=DigestAuth(self._user, self.password),
                    content=content,
                    timeout=timeout,
                )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == HTTPStatus.UNAUTHORIZED:
                raise DevicePasswordProtected from None
            raise
        except (ConnectTimeout, ConnectError, ReadTimeout, RemoteProtocolError):
            raise DeviceUnavailable from None
        else:
            return response
