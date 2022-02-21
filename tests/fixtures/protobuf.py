from typing import AsyncGenerator

import pytest_asyncio

from ..stubs.protobuf import StubProtobuf


@pytest_asyncio.fixture()
async def mock_protobuf() -> AsyncGenerator[StubProtobuf, None]:
    protobuf = StubProtobuf()
    yield protobuf
    await protobuf._session.aclose()
