"""Discover devices in your network."""

from __future__ import annotations

import asyncio
import time
from ipaddress import ip_address
from typing import Any, cast

from ifaddr import get_adapters
from zeroconf import DNSQuestionType, ServiceBrowser, ServiceStateChange, Zeroconf

from devolo_plc_api.device import Device
from devolo_plc_api.device_api import SERVICE_TYPE


async def async_discover_network(timeout: float = 3) -> dict[str, Device]:
    """
    Discover all devices that expose the devolo device API via mDNS asynchronous.

    :return: Devices accessible via serial number.
    """
    devices: dict[str, Device] = {}

    def add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        """React on state changes."""
        _add(zeroconf, service_type, name, state_change, devices=devices, timeout=timeout)

    browser = ServiceBrowser(Zeroconf(interfaces=_interfaces()), SERVICE_TYPE, [add], question_type=DNSQuestionType.QM)
    await asyncio.sleep(timeout)
    browser.cancel()
    return devices


def discover_network(timeout: float = 3) -> dict[str, Device]:
    """
    Discover devices that expose the devolo device API via mDNS synchronous.

    :return: Devices accessible via serial number.
    """
    devices: dict[str, Device] = {}

    def add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        """React on state changes."""
        _add(zeroconf, service_type, name, state_change, devices=devices, timeout=timeout)

    browser = ServiceBrowser(Zeroconf(interfaces=_interfaces()), SERVICE_TYPE, [add], question_type=DNSQuestionType.QM)
    time.sleep(timeout)
    browser.cancel()
    return devices


def _add(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange, **kwargs: Any) -> None:
    """Create a device object to each matching device."""
    if state_change is not ServiceStateChange.Added:
        return

    if (service_info := zeroconf.get_service_info(service_type, name, timeout=kwargs["timeout"] * 1000)) is None:
        return

    info = Device.info_from_service(service_info)
    if info is None or info.properties["MT"] in ("2600", "2601"):
        return  # Don't react on devolo Home Control central units

    devices: dict[str, Device] = kwargs["devices"]
    devices[info.properties["SN"]] = Device(ip=str(ip_address(info.address)), zeroconf_instance=zeroconf)


def _interfaces() -> list[str]:
    """Get IP addresses not being localhost."""
    interface: list[str] = []
    for adapter in get_adapters():
        interface.extend(cast("str", ip.ip) for ip in adapter.ips if ip.is_IPv4 and ip.ip != "127.0.0.1")
        interface.extend(cast("str", ip.ip[0]) for ip in adapter.ips if ip.is_IPv6 and ip.ip[0] != "::1")
    return interface
