from fastapi import APIRouter, HTTPException, Request, status

from app.api.schemes import ErrorSchema, IsReady
from app.constants import SERVICE_UNAVAILABLE

router = APIRouter()


@router.get(
    '/healthz/ready',
    responses={200: {'model': IsReady}, 503: {'model': ErrorSchema}},
)
async def check_health(request: Request):
    """Health check endpoint."""
    unavailable_services = []
    try:
        if not await request.app.state.auth_client.check_health():
            unavailable_services.append('Auth service')
    except Exception:
        unavailable_services.append('Auth service')
    try:
        if not await request.app.state.transaction_client.check_health():
            unavailable_services.append('Transaction service')
    except Exception:
        unavailable_services.append('Transaction service')
    if unavailable_services:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=SERVICE_UNAVAILABLE.format(services=unavailable_services),
        )
    return IsReady(is_ready=True)
