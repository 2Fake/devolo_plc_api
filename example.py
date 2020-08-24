import asyncio

from aiohttp import ClientSession

from devolo_plc_api.device import Device


# IP of the device to query
IP = "192.168.0.10"


async def run():
    async with Device(IP) as dpa:

        # Get details about wifi guest access
        print(await dpa.device.get_wifi_guest_access())

        # Get PLC data rates
        print(await dpa.plcnet.get_network_overview())


if __name__ == "__main__":
    asyncio.run(run())
