import asyncio

from aiohttp import ClientSession

from devolo_plc_api.devolo_plc_api import DevoloPlcApi

IP = "192.168.178.35"


async def run():
    async with ClientSession() as session:
        dpa = DevoloPlcApi(IP, session)
        print(await dpa.device_api.wifi1.get_wifi_guest_access())
        print(await dpa.plc_net_api.get_network_overview())


if __name__ == "__main__":
    asyncio.run(run())
