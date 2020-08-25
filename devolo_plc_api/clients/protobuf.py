class Protobuf:
    """
    Google Protobuf client.
    """

    @property
    def url(self):
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"

    async def async_get(self, sub_url):
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        return await self._session.get(url)

    def get(self, sub_url):
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Calling {url}")
        return self._session.get(url)