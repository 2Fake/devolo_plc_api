class Protobuf:
    """
    Google Protobuf client.
    """

    @property
    def url(self):
        """ The URL to query. """
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"


    async def async_get(self, sub_url):
        """ Query URL asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        return await self._session.get(url)

    async def async_post(self, sub_url):
        from requests.auth import HTTPDigestAuth
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        headers = {"realm":"devolo-api"}
        return await self._session.post(url, auth=aiohttp.BasicAuth("devolo", "oloved03"), headers=headers)

    def get(self, sub_url):
        """ Query URL synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        return self._session.get(url)
