class Protobuf:

    async def get(self, sub_url):
        return await self._session.get(f"http://{self._ip}:{self._port}/{self._path}/{self._version}/{sub_url}")
