from fastapi import APIRouter, Depends
from httpx import AsyncClient
from fastapi.responses import JSONResponse

from app.api.schemes import (
    FaceVerificationRequest,
    FaceVerificationResponse,
    ErrorSchema,
)
from app.constants import EMBEDDING_LINK
from app.service import check_token, get_client_face_verification

router = APIRouter()


@router.post(
    EMBEDDING_LINK,
    response_model=FaceVerificationResponse,
    response_model_exclude={'user_id'},
    responses={400: {'model': ErrorSchema}},
)
async def create_transaction(
    user_data: FaceVerificationRequest,
    client: AsyncClient = Depends(get_client_face_verification),
    user_id: int = Depends(check_token),
):
    """Эндпоинт создания эмбеддинга."""
    request_data = user_data.model_dump()
    request_data['user_id'] = user_id
    response = await client.post(EMBEDDING_LINK, json=request_data)
    return JSONResponse(
        status_code=response.status_code,
        content=response.json(),
    )
