from fastapi import APIRouter, Depends
from httpx import AsyncClient

from src.app.api.schemes import (
    FaceVerificationRequest,
    FaceVerificationResponse,
)
from src.app.constants import EMBEDDING_LINK
from src.app.service import check_token, get_client_face_verification

router = APIRouter()


@router.post(
    EMBEDDING_LINK,
    response_model=FaceVerificationResponse,
    response_model_exclude=['user_id'],
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
    return response.json()
