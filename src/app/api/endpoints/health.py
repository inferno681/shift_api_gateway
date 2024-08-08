from fastapi import APIRouter, Depends, HTTPException, status
from httpx import AsyncClient

from app.api.schemes import ErrorSchema, IsReady
from app.constants import HEALTH_LINK, SERVICE_UNAVAILABLE
from app.service import get_client_auth, get_client_transaction

router = APIRouter()


@router.get(
    '/healthz/ready',
    responses={200: {'model': IsReady}, 503: {'model': ErrorSchema}},
)
async def check_health(
    client_auth: AsyncClient = Depends(get_client_auth),
    client_transaction: AsyncClient = Depends(get_client_transaction),
):
    """Эндпоинт проверки запущен ли сервис."""
    unavailable_services = []
    try:
        if (
            await client_auth.get(HEALTH_LINK)
        ).status_code != status.HTTP_200_OK:
            unavailable_services.append('Сервис авторизации')
    except Exception:
        unavailable_services.append('Сервис авторизации')
    try:
        if (
            await client_transaction.get(HEALTH_LINK)
        ).status_code != status.HTTP_200_OK:
            unavailable_services.append('Сервис транзакций')
    except Exception:
        unavailable_services.append('Сервис транзакций')
    if unavailable_services:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=SERVICE_UNAVAILABLE.format(services=unavailable_services),
        )
    return IsReady(is_ready=True)
