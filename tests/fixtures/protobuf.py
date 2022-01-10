from http import HTTPStatus
from typing import AsyncGenerator

import pytest
from httpx import ConnectTimeout, HTTPStatusError, Request, Response
from pytest_httpx import HTTPXMock

from ..stubs.protobuf import StubProtobuf


@pytest.fixture()
async def mock_protobuf() -> AsyncGenerator[StubProtobuf, None]:
    protobuf = StubProtobuf()
    yield protobuf
    await protobuf._session.aclose()


@pytest.fixture()
def mock_device_unavailable(httpx_mock: HTTPXMock) -> None:

    def raise_type_error(request: Request):
        raise ConnectTimeout(request=request, message=request.extensions)

    httpx_mock.add_callback(raise_type_error)


@pytest.fixture()
def mock_wrong_password(httpx_mock: HTTPXMock) -> None:

    def raise_type_error(request: Request):
        raise HTTPStatusError(request=request,
                              message=request.extensions,
                              response=Response(status_code=HTTPStatus.UNAUTHORIZED))

    httpx_mock.add_callback(raise_type_error)
