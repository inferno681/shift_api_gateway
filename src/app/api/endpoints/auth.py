from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from opentracing import Format, global_tracer

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
    request: Request,
    client: AsyncClient = Depends(get_client_auth),
):
    """Эндпоинт регистрации пользователя."""
    with global_tracer().start_active_span('registration') as scope:
        data = await request.json()
        scope.span.set_tag('registration_data', str(data))
        headers: dict[str, str] = {}
        global_tracer().inject(
            scope.span.context,
            Format.HTTP_HEADERS,
            headers,
        )
        response = await client.post(
            REGISTRATION_LINK,
            json=user.model_dump(),
            headers=headers,
        )
        scope.span.set_tag('response_status', response.status_code)
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
    request: Request,
    client: AsyncClient = Depends(get_client_auth),
):
    """Эндпоинт аутентификации пользователя."""
    with global_tracer().start_active_span('login') as scope:
        data = await request.json()
        scope.span.set_tag('login_data', str(data))
        headers: dict[str, str] = {}
        global_tracer().inject(
            scope.span.context,
            Format.HTTP_HEADERS,
            headers,
        )
        response = await client.post(
            AUTH_LINK,
            json=user.model_dump(),
            headers=headers,
        )
        scope.span.set_tag('response_status', response.status_code)
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
    file_bytes = await file.read()
    await client.post(
        PHOTO_UPLOAD_LINK,
        data={'user_id': user_id},
        files={'file': (file.filename, file_bytes, file.content_type)},
    )
    return KafkaResponse
