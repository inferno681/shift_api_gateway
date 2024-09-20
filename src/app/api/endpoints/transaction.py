from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from opentracing import global_tracer

from app.api.schemes import (
    ErrorSchema,
    Transaction,
    TransactionCreate,
    TransactionReport,
    TransactionReportCreate,
)
from app.constants import CREATE_REPORT_LINK, CREATE_TRANSACTION_LINK
from app.service import check_token

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
    request: Request,
    user_id: int = Depends(check_token),
):
    """Transaction creation endpoint."""
    with global_tracer().start_active_span('create_transaction') as scope:
        request_data = transaction.model_dump()
        request_data['user_id'] = user_id
        scope.span.set_tag('request_data', str(request_data))
        response_data, status_code = (
            await request.app.state.transaction_client.create_transaction(
                request_data,
            )
        )
        scope.span.set_tag('status', status_code)
        return JSONResponse(
            status_code=status_code,
            content=response_data,
        )


@router.post(
    CREATE_REPORT_LINK,
    response_model=TransactionReport,
    response_model_exclude={'user_id'},
    responses={400: {'model': ErrorSchema}},
)
async def create_report(
    report_data: TransactionReportCreate,
    request: Request,
    user_id: int = Depends(check_token),
):
    """Report creation endpoint."""
    with global_tracer().start_active_span('create_report') as scope:
        request_data = jsonable_encoder(report_data)
        request_data['user_id'] = user_id
        scope.span.set_tag('request_data', request_data)
        response_data, status_code = (
            await request.app.state.transaction_client.create_report(
                request_data,
            )
        )
        scope.span.set_tag('status', status_code)
        return JSONResponse(
            status_code=status_code,
            content=response_data,
        )
