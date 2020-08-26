from httpx import DigestAuth


class Protobuf:
    """
    Google Protobuf client. This client is not usable stand alone but needs to be derived.
    """

    @property
    def url(self):
        """ The base URL to query. """
        return f"http://{self._ip}:{self._port}/{self._path}/{self._version}/"


    async def async_get(self, sub_url):
        """ Query URL asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Getting from {url}")
        return await self._session.get(url, auth=DigestAuth(self._user, self._password))

    def get(self, sub_url):
        """ Query URL synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Getting from {url}")
        return self._session.get(url, auth=DigestAuth(self._user, self._password))

    async def async_post(self, sub_url, data):
        """ Post data asynchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Posting to {url}")
        return await self._session.post(url, auth=DigestAuth(self._user, self._password), data=data)

    def post(self, sub_url, data):
        """ Post data synchronously. """
        url = f"{self.url}{sub_url}"
        self._logger.debug(f"Posting to {url}")
        return self._session.post(url, auth=DigestAuth(self._user, self._password), data=data)
