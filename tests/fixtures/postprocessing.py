"""Fixtures for postprocessing tests."""

from __future__ import annotations

import pytest

from devolo_plc_api.device_api import SupportInfoDump, SupportInfoItem

CONFIGLAYER = {
    "DIDMNG.GENERAL.DIDS": "0,1,2",
    "DIDMNG.GENERAL.WIRE_LENGTH": "0,97,0",
    "MASTERSELECTION.DOMAIN.LOST_MAPS": "178",
    "NDIM.GENERAL.N_VISIBLE_DOMAINS": "1",
    "NODE.GENERAL.NUM_HOPS": "1",
    "NODE.GENERAL.PROXY_DEVICE_ID": "1",
    "TEMPSENSORS.GENERAL.MEASURE": "7090",
}

NODE_TYPE = {
    "END_POINT": {},
    "DOMAIN_MASTER": {
        "DIDMNG.GENERAL.WIRE_LENGTH": "0,0,97",
        "MASTERSELECTION.DOMAIN.LOST_MAPS": "0",
        "NODE.GENERAL.NUM_HOPS": "0",
        "NODE.GENERAL.PROXY_DEVICE_ID": "0",
    },
    "ALONE": {
        "DIDMNG.GENERAL.DIDS": "0,1",
        "DIDMNG.GENERAL.WIRE_LENGTH": "0,0",
    },
}


def _support_info(label: str, values: dict[str, str]) -> SupportInfoDump:
    """Generate a support information dump holding the given values in the given item."""
    content = "\n".join(f"{key}={value}" for key, value in values.items())
    return SupportInfoDump(items=[SupportInfoItem(label=label, content=content.encode())])


@pytest.fixture
def support_info(node_type: str) -> SupportInfoDump:
    """Generate mocked support information of a device being end point, domain master or alone in its PLC network."""
    return _support_info("configlayer", CONFIGLAYER | NODE_TYPE[node_type])


@pytest.fixture(scope="session")
def unsupported_support_info() -> SupportInfoDump:
    """Generate mocked support information of a device not reporting any known value."""
    return _support_info("configlayer", {"UNKNOWN.GENERAL.VALUE": "1"})


@pytest.fixture(scope="session")
def foreign_support_info() -> SupportInfoDump:
    """Generate mocked support information reporting its values in another item than the configlayer."""
    return _support_info("test", CONFIGLAYER)
