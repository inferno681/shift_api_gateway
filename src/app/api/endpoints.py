from fastapi import APIRouter, Depends
from httpx import AsyncClient

from src.app.api.schemes import (
    UserCreate,
    UserToken,
    UserTokenCheck,
    UserTokenCheckRequest,
)
from src.app.constants import AUTH_LINK, CHECK_TOKEN_LINK, REGISTRATION_LINK
from src.app.service import get_client_auth

router = APIRouter()


@router.post(REGISTRATION_LINK, response_model=UserToken)
async def registration(
    user: UserCreate,
    client: AsyncClient = Depends(get_client_auth),
):
    """Эндпоинт регистрации пользователя."""
    response = await client.post(REGISTRATION_LINK, json=user.model_dump())
    return response.json()


@router.post(AUTH_LINK, response_model=UserToken)
async def authentication(
    user: UserCreate,
    client: AsyncClient = Depends(get_client_auth),
):
    """Эндпоинт аутентификации пользователя."""
    return await client.post(AUTH_LINK, json=user.model_dump())


@router.post(CHECK_TOKEN_LINK, response_model=UserTokenCheck)
async def check_token(
    token: UserTokenCheckRequest,
    client: AsyncClient = Depends(get_client_auth),
):
    """Эндпоинт проверки токена пользователя."""
    return await client.post(CHECK_TOKEN_LINK, json=token.model_dump())
