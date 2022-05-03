"""Discover devices in your network."""
from __future__ import annotations

import asyncio
import time

from zeroconf import DNSQuestionType, ServiceBrowser, ServiceStateChange, Zeroconf

from ..device import Device
from ..device_api import SERVICE_TYPE


async def async_discover_network() -> dict[str, Device]:
    """
    Discover all devices that expose the devolo device API via mDNS asynchronous.

    :return: Devices accessible via serial number.
    """
    devices: dict[str, Device] = {}

    def add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        """React on state changes."""
        _add(devices, zeroconf, service_type, name, state_change)

    browser = ServiceBrowser(Zeroconf(), SERVICE_TYPE, [add], question_type=DNSQuestionType.QM)
    await asyncio.sleep(3)
    browser.cancel()
    return devices


def discover_network() -> dict[str, Device]:
    """
    Discover devices that expose the devolo device API via mDNS synchronous.

    :return: Devices accessible via serial number.
    """
    devices: dict[str, Device] = {}

    def add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        """React on state changes."""
        _add(devices, zeroconf, service_type, name, state_change)

    browser = ServiceBrowser(Zeroconf(), SERVICE_TYPE, [add], question_type=DNSQuestionType.QM)
    time.sleep(3)
    browser.cancel()
    return devices


def _add(
    devices: dict[str, Device], zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    """Create a device object to each matching device."""
    if state_change is not ServiceStateChange.Added:
        return

    if (service_info := zeroconf.get_service_info(service_type, name)) is None:
        return

    info = Device.info_from_service(service_info)
    if info is None or info["properties"]["MT"] in ("2600", "2601"):
        return  # Don't react on devolo Home Control central units

    devices[info["properties"]["SN"]] = Device(ip=info["address"], deviceapi=info, zeroconf_instance=zeroconf)
