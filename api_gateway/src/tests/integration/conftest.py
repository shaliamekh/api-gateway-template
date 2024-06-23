import pytest_asyncio

from adapters.aihttp_gateway_router import get_session


@pytest_asyncio.fixture(scope="session")
async def http_session():
    session = await get_session()
    yield session
    await session.close()
