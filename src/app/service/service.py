from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from httpx import AsyncClient

from src.app.api.schemes import UserTokenCheck, UserTokenCheckRequest
from src.app.constants import (
    CHECK_TOKEN_LINK,
    INVALID_TOKEN_MESSAGE,
    TOKEN_EXPIRED_MESSAGE,
)
from src.config import config

header_scheme = APIKeyHeader(name='Authorization')


async def get_client_face_verification():
    """Клиент для запросов к face_verification_service."""
    async with AsyncClient(
        base_url=config.face_verification.base_url,
    ) as client:
        yield client


async def get_client_transaction():
    """Клиент для запросов к transaction_service."""
    async with AsyncClient(
        base_url=config.transaction_service.base_url,
    ) as client:
        yield client


async def get_client_auth():
    """Клиент для запросов к auth_service."""
    async with AsyncClient(
        base_url=config.auth_service.base_url,
    ) as client:
        yield client


async def check_token(
    token: str = Depends(header_scheme),
    client: AsyncClient = Depends(get_client_auth),
) -> int:
    """Проверка токена пользователя."""
    token = UserTokenCheckRequest(token=token)
    response = await client.post(CHECK_TOKEN_LINK, json=token.model_dump())
    response_data = response.json()
    if response.status_code == status.HTTP_400_BAD_REQUEST and (
        response_data.get('detail') == INVALID_TOKEN_MESSAGE
        or TOKEN_EXPIRED_MESSAGE
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response_data['detail'],
        )
    result = UserTokenCheck(**response_data)
    if not result.is_token_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_TOKEN_MESSAGE,
        )
    return result.user_id
