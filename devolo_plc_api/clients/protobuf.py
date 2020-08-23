class Protobuf:
    """
    Google Protobuf client.
    """

    async def get(self, sub_url):
        url = f"http://{self._ip}:{self._port}/{self._path}/{self._version}/{sub_url}"
        self._logger.debug(f"Calling {url}")
        return await self._session.get(url)
