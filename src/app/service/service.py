from fastapi import Depends, HTTPException, Request, UploadFile, status
from fastapi.security import APIKeyHeader
from httpx import AsyncClient
from opentracing import Format, global_tracer

from app.api.schemes import UserTokenCheck
from app.constants import (
    AUTH_LINK,
    CHECK_TOKEN_LINK,
    CREATE_REPORT_LINK,
    CREATE_TRANSACTION_LINK,
    HEALTH_LINK,
    INVALID_TOKEN_MESSAGE,
    PHOTO_UPLOAD_LINK,
    REGISTRATION_LINK,
)

header_scheme = APIKeyHeader(name='Authorization')


class ServiceClient:
    """Базовый клиент для отправки запросов."""

    def __init__(self, base_url: str):
        """Инициализация клиента."""
        self.client = AsyncClient()
        self.base_url = base_url

    async def check_health(self) -> bool:
        """Метод выполнения GET запроса для проверки готовности сервиса."""
        url = f'{self.base_url}{HEALTH_LINK}'
        response = await self.client.get(url)
        return response.status_code == status.HTTP_200_OK

    async def post(self, path: str, **kwargs):
        """Метод выполнения POST запроса с добавлением хэдеров трейсинга."""
        url = f'{self.base_url}{path}'
        headers = kwargs.get('headers', {})

        span = global_tracer().active_span
        if span:
            global_tracer().inject(span.context, Format.HTTP_HEADERS, headers)

        kwargs['headers'] = headers

        response = await self.client.post(url, **kwargs)
        return response.json(), response.status_code

    async def aclose(self):
        """Метод закрытия клиента."""
        await self.client.aclose()


class AuthServiceClient(ServiceClient):
    """Клиент для запросов к сервису авторизации."""

    async def registration(self, data):
        """Запрос регистрации пользователя."""
        return await self.post(REGISTRATION_LINK, json=data)

    async def login(self, data):
        """Запрос аутентификации пользователя."""
        return await self.post(AUTH_LINK, json=data)

    async def check_token(self, token: str) -> int | None:
        """Запрос для проверки токена."""
        return await self.post(CHECK_TOKEN_LINK, json={'token': token})

    async def verify(self, user_id: int, file: UploadFile):
        """Запрос загрузки фото для верификации."""
        return await self.post(
            PHOTO_UPLOAD_LINK,
            data={'user_id': user_id},
            files={
                'file': (file.filename, await file.read(), file.content_type),
            },
        )


class TransactionServiceClient(ServiceClient):
    """Клиент для запросов к сервису авторизации."""

    async def create_transaction(self, data):
        """Запрос создания транзакции."""
        return await self.post(CREATE_TRANSACTION_LINK, json=data)

    async def create_report(self, data):
        """Запрос создания отчета."""
        return await self.post(CREATE_REPORT_LINK, json=data)


async def check_token(
    request: Request,
    token: str = Depends(header_scheme),
) -> int | None:
    """Проверка токена пользователя."""
    with global_tracer().start_active_span('check_token') as scope:
        scope.span.set_tag('token', token[:10] + '...')
        response_data, status_code = (
            await request.app.state.auth_client.check_token(token)
        )
        scope.span.set_tag('response_status', status_code)
        if status_code != status.HTTP_200_OK:
            scope.span.set_tag('error', response_data['detail'])
            raise HTTPException(
                status_code=status_code,
                detail=response_data['detail'],
            )
        result = UserTokenCheck(**response_data)
        if not result.is_token_valid:
            scope.span.set_tag('error', INVALID_TOKEN_MESSAGE)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_TOKEN_MESSAGE,
            )
        return result.user_id
