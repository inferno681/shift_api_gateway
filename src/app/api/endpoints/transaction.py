from fastapi import APIRouter, Depends, Header
from httpx import AsyncClient

from src.app.api.schemes import (
    Transaction,
    TransactionCreate,
    TransactionReport,
    TransactionReportCreate,
)
from src.app.constants import CREATE_TRANSACTION_LINK, CREATE_REPORT_LINK
from src.app.service import get_client_auth, check_token

router = APIRouter()


@router.post(CREATE_TRANSACTION_LINK, response_model=Transaction)
async def create_transaction(
    transaction: TransactionCreate,
    client: AsyncClient = Depends(get_client_auth),
    user_id: int = Depends(check_token),
):
    """Эндпоинт создания транзакции."""
    request_data = transaction.model_dump()
    request_data['user_id'] = user_id
    response = await client.post(CREATE_TRANSACTION_LINK, json=request_data)
    return response.json()
