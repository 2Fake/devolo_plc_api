import asyncio

from aiohttp import ClientSession

from devolo_plc_api.devolo_plc_api import DevoloPlcApi

IP = "http://192.168.178.35"
PORT = 14791


async def run():
    async with ClientSession() as session:
        dpa = DevoloPlcApi(IP, session, PORT)
        print(await dpa.get_wifi_guest_access())


if __name__ == "__main__":
    asyncio.run(run())
