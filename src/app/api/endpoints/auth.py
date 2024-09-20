from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from httpx import AsyncClient

from app.api.schemes import ErrorSchema, UserCreate, UserToken
from app.constants import AUTH_LINK, REGISTRATION_LINK
from app.service import get_client_auth

router = APIRouter()


@router.post(
    REGISTRATION_LINK,
    response_model=UserToken,
    responses={400: {'model': ErrorSchema}},
)
async def registration(
    user: UserCreate,
    client: AsyncClient = Depends(get_client_auth),
):
    """Эндпоинт регистрации пользователя."""
    response = await client.post(REGISTRATION_LINK, json=user.model_dump())
    return JSONResponse(
        status_code=response.status_code,
        content=response.json(),
    )


@router.post(
    AUTH_LINK,
    response_model=UserToken,
    responses={404: {'model': ErrorSchema}},
)
async def authentication(
    user: UserCreate,
    client: AsyncClient = Depends(get_client_auth),
):
    """Эндпоинт аутентификации пользователя."""
    response = await client.post(AUTH_LINK, json=user.model_dump())
    return JSONResponse(
        status_code=response.status_code,
        content=response.json(),
    )
