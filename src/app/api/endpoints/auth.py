from fastapi import APIRouter, Depends
from httpx import AsyncClient

from src.app.api.schemes import UserCreate, UserToken
from src.app.constants import AUTH_LINK, REGISTRATION_LINK
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
    response = await client.post(AUTH_LINK, json=user.model_dump())
    return response.json()
