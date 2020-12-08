import asyncio
import time
from typing import Dict

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from ..device import Device

_devices: Dict[str,
               Device] = {}


async def async_discover_network() -> Dict[str, Device]:
    """
    Discover all devices that expose the devolo device API via mDNS asynchronous.

    :return: Devices accessible via serial number.
    """
    browser = ServiceBrowser(Zeroconf(), "_dvl-deviceapi._tcp.local.", [_add])
    await asyncio.sleep(3)
    browser.cancel()
    return _devices


def discover_network() -> Dict[str, Device]:
    """
    Discover devices that expose the devolo device API via mDNS synchronous.

    :return: Devices accessible via serial number.
    """
    browser = ServiceBrowser(Zeroconf(), "_dvl-deviceapi._tcp.local.", [_add])
    time.sleep(3)
    browser.cancel()
    return _devices


def _add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
    """" Create a device object to each matching device. """
    if state_change is not ServiceStateChange.Added:
        return

    service_info = zeroconf.get_service_info(service_type, name)
    if service_info is None:
        return

    info = Device.info_from_service(service_info)
    if info is None or info["properties"]["MT"] in ("2600", "2601"):
        return  # Don't react on devolo Home Control central units

    _devices[info["properties"]["SN"]] = Device(ip=info["address"], deviceapi=info, zeroconf_instance=zeroconf)
