from fastapi import APIRouter, Depends
from httpx import AsyncClient
from fastapi.encoders import jsonable_encoder
from app.api.schemes import (
    Transaction,
    TransactionCreate,
    TransactionReport,
    TransactionReportCreate,
)
from app.constants import CREATE_REPORT_LINK, CREATE_TRANSACTION_LINK
from app.service import check_token, get_client_transaction

router = APIRouter()


@router.post(
    CREATE_TRANSACTION_LINK,
    response_model=Transaction,
    response_model_exclude=['user_id'],
)
async def create_transaction(
    transaction: TransactionCreate,
    client: AsyncClient = Depends(get_client_transaction),
    user_id: int = Depends(check_token),
):
    """Эндпоинт создания транзакции."""
    request_data = transaction.model_dump()
    request_data['user_id'] = user_id
    response = await client.post(CREATE_TRANSACTION_LINK, json=request_data)
    return response.json()


@router.post(CREATE_REPORT_LINK, response_model=TransactionReport)
async def create_report(
    report_data: TransactionReportCreate,
    client: AsyncClient = Depends(get_client_transaction),
    user_id: int = Depends(check_token),
):
    """Эндпоинт создания отчета."""
    request_data = jsonable_encoder(report_data)
    request_data['user_id'] = user_id
    response = await client.post(CREATE_REPORT_LINK, json=request_data)
    return response.json()
