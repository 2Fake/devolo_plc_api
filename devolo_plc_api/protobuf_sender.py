class ProtobufSender:
    def __init__(self, ip, session, port, api_type, token):
        self.ip = ip
        self.port = port
        self.session = session
        self.token = token
        self.api_type = api_type

    async def get(self, sub_url, data=None):
        return await self.session.get(f"http://{self.ip}:{self.port}/{self.token}/{self.api_type}/v0/{sub_url}")