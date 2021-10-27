from unittest.mock import AsyncMock


class MockServiceBrowser:

    async_cancel = AsyncMock()

    def __init__(self, zc, st, sc, question_type=None) -> None:
        sc[0]()
