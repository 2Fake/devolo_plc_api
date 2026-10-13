"""Typed diagnostic information from a device support dump."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .support_pb2 import SupportInfoDump

CONFIGLAYER_FORMAT = re.compile(rb"(([A-Z][A-Z0-9._]+)=(.+?))(?=(([A-Z][A-Z0-9._]+)=(.+))|$)", re.DOTALL)

_ACTIVE_SLOTS = b"MSPS.L1.ACTIVE_SLOTS"
_ACTIVE_SLOTS_MAX = b"MSPS.L1.ACTIVE_SLOTS_MAX"
_ACTIVE_SLOTS_MIN = b"MSPS.L1.ACTIVE_SLOTS_MIN"
_CONNECTED_TO_GATEWAY = b"DEVOLO.ETHERNET.CONNECTED_TO_GATEWAY"
_CPU_USAGE = b"SYSTEM.STATS.CPU_USAGE"
_ETHERNET_FULL_DUPLEX = b"DEVOLO.ETHERNET.ETH_PORTS_FULLDUPLEX"
_ETHERNET_LINK = b"DEVOLO.ETHERNET.ETH_PORTS_LINK"
_ETHERNET_SPEED = b"DEVOLO.ETHERNET.ETH_PORTS_SPEED"
_FREE_MEMORY = b"SYSTEM.STATS.FREE_MEMORY"
_LOST_MAPS = b"MASTERSELECTION.DOMAIN.LOST_MAPS"
_TEMPERATURE = b"TEMPSENSORS.GENERAL.MEASURE"
_TOTAL_MEMORY = b"SYSTEM.STATS.TOTAL_MEMORY"


@dataclass(frozen=True)
class EthernetPortDiagnostics:
    """Diagnostic information for one Ethernet port."""

    port: int
    link: bool | None
    speed_mbps: int | None
    full_duplex: bool | None


@dataclass(frozen=True)
class DeviceDiagnostics:
    """Typed diagnostic information reported by a device."""

    cpu_usage_percent: int | None = None
    total_memory_kib: int | None = None
    free_memory_kib: int | None = None
    temperature_celsius: float | None = None
    active_time_slots_percent: float | None = None
    ethernet_ports: tuple[EthernetPortDiagnostics, ...] = ()
    connected_to_gateway: bool | None = None
    lost_maps: int | None = None


def _get_int(values: dict[bytes, bytes], key: bytes) -> int | None:
    try:
        return int(values[key])
    except (KeyError, ValueError):
        return None


def _get_bool(values: dict[bytes, bytes], key: bytes) -> bool | None:
    value = values.get(key)
    if value == b"YES":
        return True
    if value == b"NO":
        return False
    return None


def _get_list(values: dict[bytes, bytes], key: bytes) -> list[bytes]:
    value = values.get(key)
    return value.split(b",") if value else []


def _get_list_int(values: list[bytes], index: int) -> int | None:
    try:
        return int(values[index])
    except (IndexError, ValueError):
        return None


def _get_list_bool(values: list[bytes], index: int) -> bool | None:
    try:
        value = values[index]
    except IndexError:
        return None
    if value == b"YES":
        return True
    if value == b"NO":
        return False
    return None


def _parse_configlayer(support_info: SupportInfoDump) -> dict[bytes, bytes]:
    values: dict[bytes, bytes] = {}
    for item in support_info.items:
        if item.label != "configlayer":
            continue
        for match in CONFIGLAYER_FORMAT.finditer(item.content):
            values[match.group(2)] = match.group(3).strip()
    return values


def _parse_device_diagnostics(support_info: SupportInfoDump) -> DeviceDiagnostics:
    values = _parse_configlayer(support_info)

    temperature = _get_int(values, _TEMPERATURE)
    active_slots = _get_int(values, _ACTIVE_SLOTS)
    active_slots_min = _get_int(values, _ACTIVE_SLOTS_MIN)
    active_slots_max = _get_int(values, _ACTIVE_SLOTS_MAX)
    active_time_slots_percent = None
    if active_slots is not None and active_slots_max is not None and active_slots_max > 0:
        active_time_slots_percent = max(active_slots, active_slots_min or 0) / active_slots_max * 100

    links = _get_list(values, _ETHERNET_LINK)
    speeds = _get_list(values, _ETHERNET_SPEED)
    full_duplex = _get_list(values, _ETHERNET_FULL_DUPLEX)
    ethernet_ports = tuple(
        EthernetPortDiagnostics(
            port=index + 1,
            link=_get_list_bool(links, index),
            speed_mbps=_get_list_int(speeds, index),
            full_duplex=_get_list_bool(full_duplex, index),
        )
        for index in range(max(len(links), len(speeds), len(full_duplex)))
    )

    return DeviceDiagnostics(
        cpu_usage_percent=_get_int(values, _CPU_USAGE),
        total_memory_kib=_get_int(values, _TOTAL_MEMORY),
        free_memory_kib=_get_int(values, _FREE_MEMORY),
        temperature_celsius=temperature / 100 if temperature is not None else None,
        active_time_slots_percent=active_time_slots_percent,
        ethernet_ports=ethernet_ports,
        connected_to_gateway=_get_bool(values, _CONNECTED_TO_GATEWAY),
        lost_maps=_get_int(values, _LOST_MAPS),
    )
