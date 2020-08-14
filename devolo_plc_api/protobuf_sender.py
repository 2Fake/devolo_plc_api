class ProtobufSender:
    def __init__(self, ip, session, port):
        self.ip = ip
        self.port = port
        self.session = session
        self.token = "1e6be8c2bb7ac289"

    async def get(self, sub_url, data=None):
        return await self.session.get(f"{self.ip}:{self.port}/{self.token}/deviceapi/v0/{sub_url}")