from unittest.mock import AsyncMock


class MockServiceBrowser:

    async_cancel = AsyncMock()

    def __init__(self, zeroconf, type_, handlers, addr, question_type=None) -> None:
        handlers[0]()
