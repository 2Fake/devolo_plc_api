import asyncio
import json
import pathlib
from typing import Generator

import pytest

pytest_plugins = [
    "tests.fixtures.device",
    "tests.fixtures.device_api",
    "tests.fixtures.plcnet_api",
    "tests.fixtures.protobuf",
]

file = pathlib.Path(__file__).parent / "test_data.json"
with file.open("r") as fh:
    test_data = json.load(fh)


@pytest.fixture(autouse=True, scope="class")
def test_data_fixture(request: pytest.FixtureRequest) -> None:
    """Load test data."""
    request.cls.device_info = test_data["device_info"]
    request.cls.ip = test_data["ip"]


@pytest.fixture()
def event_loop() -> Generator[asyncio.events.AbstractEventLoop, None, None]:
    """Handle the event loop in tests."""
    loop = asyncio.new_event_loop()
    yield loop
    if loop.is_running():
        to_cancel = asyncio.tasks.all_tasks(loop)
        for task in to_cancel:
            task.cancel()
        loop.run_until_complete(asyncio.tasks.gather(*to_cancel, return_exceptions=True))
        loop.close()
