from httpx import DigestAuth

class Protobuf:
    """
    Google Protobuf client.
    """

    @property
    def url(self):
        """ The base URL to query. """
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"


    async def async_get(self, sub_url):
        """ Query URL asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        return await self._session.get(url)

    async def async_post(self, sub_url, data):
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        return await self._session.post(url, auth=DigestAuth("USER", "PASSWORD"), data=data)

    def get(self, sub_url):
        """ Query URL synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        return self._session.get(url)
