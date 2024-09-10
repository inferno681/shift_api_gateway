from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app


@pytest.fixture(scope='session')
def anyio_backend():
    """Бэкэнд для тестирования."""
    return 'asyncio'


@pytest.fixture(scope='session')
async def client():
    """Фикстура клиента для подключения к тестовому серверу."""
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://127.0.0.1:8000/api/',
        ) as client:
            yield client
