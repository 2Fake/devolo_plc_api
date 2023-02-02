"""Fixtures for protobuf tests."""
from collections.abc import AsyncGenerator

import pytest_asyncio

from tests.stubs.protobuf import StubProtobuf


@pytest_asyncio.fixture()
async def mock_protobuf() -> AsyncGenerator[StubProtobuf, None]:
    """Use protobuf stub."""
    protobuf = StubProtobuf()
    yield protobuf
    await protobuf.close_session()
