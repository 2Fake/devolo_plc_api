"""Fixture for protobuf tests."""
from typing import AsyncGenerator

import pytest_asyncio

from ..stubs.protobuf import StubProtobuf


@pytest_asyncio.fixture()
async def mock_protobuf() -> AsyncGenerator[StubProtobuf, None]:
    """Use protobuf stub."""
    protobuf = StubProtobuf()
    yield protobuf
    await protobuf.close_session()
