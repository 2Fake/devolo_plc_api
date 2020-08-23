import asyncio

from aiohttp import ClientSession

from devolo_plc_api.device import Device


IP = "192.168.3.13"


async def run():
    async with ClientSession() as session:
        dpa = Device(IP, session)
        print(await dpa.device.get_wifi_guest_access())
        print(await dpa.plcnet.get_network_overview())


if __name__ == "__main__":
    asyncio.run(run())
