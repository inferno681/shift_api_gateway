from httpx import AsyncClient

from src.config import config


async def get_client_face_verification():
    """Клиент для запросов к face_verification_service."""
    async with AsyncClient(
        base_url=config.base_url.face_verification,
    ) as client:
        yield client


async def get_client_transaction():
    """Клиент для запросов к transaction_service."""
    async with AsyncClient(
        base_url=config.base_url.transaction_service,
    ) as client:
        yield client


async def get_client_auth():
    """Клиент для запросов к auth_service."""
    async with AsyncClient(
        base_url=config.base_url.auth_service,
    ) as client:
        yield client
