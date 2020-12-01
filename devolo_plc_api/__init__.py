import asyncio
import time

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from .device import Device

__version__ = "0.2.0"


async def async_discover_network():
    devices = {}

    def add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """ Create a device object to each matching device. """
        if state_change is ServiceStateChange.Added:
            service_info = Device.info_from_service(zeroconf.get_service_info(service_type, name))
            devices[service_info["properties"]["SN"]] = Device(ip=service_info["address"],
                                                               deviceapi=service_info,
                                                               zeroconf_instance=zeroconf)

    browser = ServiceBrowser(Zeroconf(), "_dvl-deviceapi._tcp.local.", [add])
    await asyncio.sleep(3)
    browser.cancel()
    await asyncio.gather(*[device.async_connect() for device in devices.values()])
    return devices


def discover_network():
    devices = {}

    def add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """ Create a device object to each matching device. """
        if state_change is ServiceStateChange.Added:
            service_info = Device.info_from_service(zeroconf.get_service_info(service_type, name))
            devices[service_info["properties"]["SN"]] = Device(ip=service_info["address"],
                                                               deviceapi=service_info,
                                                               zeroconf_instance=zeroconf)

    browser = ServiceBrowser(Zeroconf(), "_dvl-deviceapi._tcp.local.", [add])
    time.sleep(3)
    browser.cancel()
    [device.connect() for device in devices.values()]
    return devices
