from fastapi import Depends, Header, HTTPException
from httpx import AsyncClient

from src.app.api.schemes import UserTokenCheck, UserTokenCheckRequest
from src.app.constants import CHECK_TOKEN_LINK
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


async def check_token(
    token: str = Header(..., alias='Authorization'),
    client: AsyncClient = Depends(get_client_auth),
) -> int | None:
    """Эндпоинт проверки токена пользователя."""
    print(token)
    token = UserTokenCheckRequest(token=token)
    response = await client.post(CHECK_TOKEN_LINK, json=token.model_dump())
    result = UserTokenCheck(**response.json())
    if not result.is_token_valid:
        return None
    return result.user_id
