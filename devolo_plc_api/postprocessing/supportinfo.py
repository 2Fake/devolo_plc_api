"""
Extract single diagnostic values from a device's support information dump.

The values reported in a support information dump describe the G.hn PLC chip of a device. On devices with an own host
processor, e.g. wifi devices, the chip is just one component and its view of the world is not the view of the device.
Therefore only values, that have the same meaning on all device types, are extracted here.

Every function returns None, if the device's firmware does not report the needed value at all. As that will not change
during runtime, it is best checked once, e.g. when setting up an integration. Functions that can also return None during
runtime say so explicitly.
"""

from __future__ import annotations

import re
from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devolo_plc_api.device_api import SupportInfoDump

VALUE_FORMAT = rb"=(.+?)(?=[A-Z][A-Z0-9._]+=|\Z)"

_HOPS = b"NODE.GENERAL.NUM_HOPS"
_LOST_MAPS = b"MASTERSELECTION.DOMAIN.LOST_MAPS"
_TEMPERATURE = b"TEMPSENSORS.GENERAL.MEASURE"
_UPLINK = b"NODE.GENERAL.PROXY_DEVICE_ID"
_VISIBLE_DOMAINS = b"NDIM.GENERAL.N_VISIBLE_DOMAINS"
_WIRE_LENGTH = b"DIDMNG.GENERAL.WIRE_LENGTH"


def temperature(support_info: SupportInfoDump) -> float | None:
    """
    Get the current temperature of a device's G.hn PLC chip.

    :param support_info: Support information dump as returned by the device API
    :return: Temperature in degree celsius
    """
    value = _configlayer_value(support_info, _TEMPERATURE)
    return value / 100 if value is not None else None


def neighboring_plc_networks(support_info: SupportInfoDump) -> int | None:
    """
    Get the number of other PLC networks a device can see.

    The own PLC network is not counted.

    :param support_info: Support information dump as returned by the device API
    :return: Number of neighboring PLC networks
    """
    return _configlayer_value(support_info, _VISIBLE_DOMAINS)


def hops(support_info: SupportInfoDump) -> int | None:
    """
    Get the number of hops a device needs to reach the domain master of its PLC network.

    The domain master itself reports zero and a device connected directly to it reports one. Anything above that means,
    that the connection is relayed by another device, which usually indicates a bad connection.

    :param support_info: Support information dump as returned by the device API
    :return: Number of hops to the domain master
    """
    return _configlayer_value(support_info, _HOPS)


def wire_length(support_info: SupportInfoDump) -> int | None:
    """
    Get the estimated length of the power line between a device and the device it uplinks to.

    The length is estimated from signal runtime, so it fluctuates slightly. This value is also None during runtime, if a
    device currently has no uplink, which is the case on a domain master and on a device being alone in its PLC network.

    :param support_info: Support information dump as returned by the device API
    :return: Length of the power line in meters
    """
    if not (uplink := _configlayer_value(support_info, _UPLINK)):
        return None
    return _configlayer_value(support_info, _WIRE_LENGTH, uplink) or None


def lost_maps(support_info: SupportInfoDump) -> int | None:
    """
    Get the number of media access plans a device lost since its last start.

    Only devices, that are not the domain master of their PLC network, can lose media access plans. A domain master always
    reports zero.

    :param support_info: Support information dump as returned by the device API
    :return: Number of lost media access plans
    """
    return _configlayer_value(support_info, _LOST_MAPS)


def _configlayer_value(support_info: SupportInfoDump, key: bytes, index: int = 0) -> int | None:
    """Get a configlayer value as integer, values holding a list by index."""
    for item in support_info.items:
        if item.label == "configlayer" and (match := re.search(re.escape(key) + VALUE_FORMAT, item.content, re.DOTALL)):
            with suppress(IndexError, ValueError):
                return int(match[1].strip().split(b",")[index])
    return None
