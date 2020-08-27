from logging import Logger

from google.protobuf.json_format import MessageToDict
from httpx import DigestAuth, Response

from ..exceptions.device import DevicePasswordProtected

TIMEOUT = 3.0


class Protobuf:
    """
    Google Protobuf client. This client is not usable stand alone but needs to be derived.
    """
    _logger: Logger


    @property
    def url(self):
        """ The base URL to query. """
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"


    async def _async_get(self, sub_url: str, timeout: float = TIMEOUT) -> Response:
        """ Query URL asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Getting from {url}")
        try:
            return await self._session.get(url, auth=DigestAuth(self._user, self._password), timeout=timeout)  # type: ignore
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None

    def _get(self, sub_url: str, timeout: float = TIMEOUT) -> Response:
        """ Query URL synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Getting from {url}")
        try:
            return self._session.get(url, auth=DigestAuth(self._user, self._password, timeout=timeout))  # type: ignore
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None

    def _message_to_dict(self, message) -> dict:
        """ Convert message to dict with certain settings. """
        return MessageToDict(message=message, including_default_value_fields=True, preserving_proto_field_name=True)

    async def _async_post(self, sub_url: str, data: str, timeout: float = TIMEOUT) -> Response:
        """ Post data asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Posting to {url}")
        try:
            return await self._session.post(url, auth=DigestAuth(self._user, self._password), data=data, timeout=timeout)  # type: ignore
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None

    def _post(self, sub_url: str, data: str, timeout: float = TIMEOUT) -> Response:
        """ Post data synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Posting to {url}")
        try:
            return self._session.post(url, auth=DigestAuth(self._user, self._password), data=data, timeout=timeout)  # type: ignore
        except TypeError:
            raise DevicePasswordProtected("The used password is wrong.") from None
