from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from opentracing import Format, global_tracer

from app.api.schemes import (
    ErrorSchema,
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
    response_model_exclude={'user_id'},
    responses={
        403: {'model': ErrorSchema},
    },
)
async def create_transaction(
    transaction: TransactionCreate,
    client: AsyncClient = Depends(get_client_transaction),
    user_id: int = Depends(check_token),
):
    """Эндпоинт создания транзакции."""
    with global_tracer().start_active_span('create_transaction') as scope:
        request_data = transaction.model_dump()
        request_data['user_id'] = user_id
        scope.span.set_tag('request_data', str(request_data))
        headers: dict[str, str] = {}
        global_tracer().inject(
            scope.span.context,
            Format.HTTP_HEADERS,
            headers,
        )
        response = await client.post(
            CREATE_TRANSACTION_LINK,
            json=request_data,
            headers=headers,
        )
        scope.span.set_tag('status', response.status_code)
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )


@router.post(
    CREATE_REPORT_LINK,
    response_model=TransactionReport,
    response_model_exclude={'user_id'},
    responses={400: {'model': ErrorSchema}},
)
async def create_report(
    report_data: TransactionReportCreate,
    client: AsyncClient = Depends(get_client_transaction),
    user_id: int = Depends(check_token),
):
    """Эндпоинт создания отчета."""
    with global_tracer().start_active_span('create_report') as scope:
        request_data = jsonable_encoder(report_data)
        request_data['user_id'] = user_id
        scope.span.set_tag('request_data', request_data)
        headers: dict[str, str] = {}
        global_tracer().inject(
            scope.span.context,
            Format.HTTP_HEADERS,
            headers,
        )
        response = await client.post(
            CREATE_REPORT_LINK,
            json=request_data,
            headers=headers,
        )
        scope.span.set_tag('status', response.status_code)
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
