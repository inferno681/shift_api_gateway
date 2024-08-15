from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from httpx import AsyncClient

from app.api.schemes import ErrorSchema, KafkaResponse, UserCreate, UserToken
from app.constants import (
    AUTH_LINK,
    FILENAME_ERROR,
    PHOTO_UPLOAD_LINK,
    REGISTRATION_LINK,
)
from app.service import check_token, get_client_auth

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


@router.post(
    PHOTO_UPLOAD_LINK,
    response_model=KafkaResponse,
)
async def verify(
    user_id: int = Depends(check_token),
    client: AsyncClient = Depends(get_client_auth),
    file: UploadFile = File(),
):
    """Эндпоинт загрузки фотографии."""
    if file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FILENAME_ERROR,
        )
    await client.post(
        PHOTO_UPLOAD_LINK,
        data={'user_id': user_id},
        files={'file': (file.filename, file.file)},
    )
    return KafkaResponse
