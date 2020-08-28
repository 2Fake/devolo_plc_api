class AsyncClient:
    async def get(self, url, auth, timeout):
        pass

    async def post(self, url, auth, data, timeout):
        pass

    async def wrong_password(self, *args, **kwargs):
        raise TypeError()


class Client:
    def get(self, url, auth, timeout):
        pass

    def post(self, url, auth, data, timeout):
        pass

    def wrong_password(self, *args, **kwargs):
        raise TypeError()
