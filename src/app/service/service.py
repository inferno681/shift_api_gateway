from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from httpx import AsyncClient
from opentracing import Format, global_tracer

from app.api.schemes import UserTokenCheck
from app.constants import CHECK_TOKEN_LINK, INVALID_TOKEN_MESSAGE
from config import config

header_scheme = APIKeyHeader(name='Authorization')


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
    request: Request,
    token: str = Depends(header_scheme),
    client: AsyncClient = Depends(get_client_auth),
) -> int | None:
    """Проверка токена пользователя."""
    with global_tracer().start_active_span('check_token') as scope:
        scope.span.set_tag('token', token[:10] + '...')
        headers: dict[str, str] = {}
        global_tracer().inject(
            scope.span.context,
            Format.HTTP_HEADERS,
            headers,
        )
        response = await client.post(
            CHECK_TOKEN_LINK,
            json={'token': token},
            headers=headers,
        )
        response_data = response.json()
        scope.span.set_tag('response_status', response.status_code)
        if response.status_code != status.HTTP_200_OK:
            scope.span.set_tag('error', response_data['detail'])
            raise HTTPException(
                status_code=response.status_code,
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
