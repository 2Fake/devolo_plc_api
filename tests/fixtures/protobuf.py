import pytest
from httpx import ConnectTimeout

from ..stubs.protobuf import StubProtobuf


@pytest.fixture()
async def mock_protobuf():
    protobuf = StubProtobuf()
    yield protobuf
    await protobuf._session.aclose()


@pytest.fixture()
def mock_device_unavailable(httpx_mock):

    def raise_type_error(request, extensions):
        raise ConnectTimeout(request=request, message=extensions)

    httpx_mock.add_callback(raise_type_error)


@pytest.fixture()
def mock_wrong_password(httpx_mock):

    def raise_type_error(request, extensions):
        raise TypeError

    httpx_mock.add_callback(raise_type_error)
