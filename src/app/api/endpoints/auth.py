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
from opentracing import global_tracer

from app.api.schemes import ErrorSchema, KafkaResponse, UserCreate, UserToken
from app.constants import (
    AUTH_LINK,
    FILENAME_ERROR,
    PHOTO_UPLOAD_LINK,
    REGISTRATION_LINK,
)
from app.service import check_token

router = APIRouter()


@router.post(
    REGISTRATION_LINK,
    response_model=UserToken,
    responses={400: {'model': ErrorSchema}},
)
async def registration(
    user: UserCreate,
    request: Request,
):
    """Эндпоинт регистрации пользователя."""
    with global_tracer().start_active_span('registration') as scope:
        data = await request.json()
        scope.span.set_tag('registration_data', str(data))
        response, status_code = (
            await request.app.state.auth_client.registration(
                user.model_dump(),
            )
        )

        scope.span.set_tag('response_status', status_code)
        return JSONResponse(
            status_code=status_code,
            content=response,
        )


@router.post(
    AUTH_LINK,
    response_model=UserToken,
    responses={404: {'model': ErrorSchema}},
)
async def authentication(user: UserCreate, request: Request):
    """Эндпоинт аутентификации пользователя."""
    with global_tracer().start_active_span('login') as scope:
        data = await request.json()
        scope.span.set_tag('login_data', str(data))
        response, status_code = await request.app.state.auth_client.login(
            user.model_dump(),
        )
        scope.span.set_tag('response_status', status_code)
        return JSONResponse(
            status_code=status_code,
            content=response,
        )


@router.post(
    PHOTO_UPLOAD_LINK,
    response_model=KafkaResponse,
)
async def verify(
    request: Request,
    user_id: int = Depends(check_token),
    file: UploadFile = File(),
):
    """Эндпоинт загрузки фотографии."""
    with global_tracer().start_active_span('photo_upload') as scope:
        if file.filename is None:
            scope.span.set_tag('error', FILENAME_ERROR)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=FILENAME_ERROR,
            )
        await request.app.state.auth_client.verify(user_id=user_id, file=file)
        scope.span.set_tag('result', 'изображение отправлено')
        return KafkaResponse
