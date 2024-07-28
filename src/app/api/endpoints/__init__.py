from fastapi import APIRouter

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.face_verification import \
    router as face_verification_router
from app.api.endpoints.transaction import router as transaction_router
from config import config

router = APIRouter()

router.include_router(
    auth_router,
    prefix='/auth',
    tags=[config.auth_service.tags_metadata['name']],  # type: ignore
)
router.include_router(
    transaction_router,
    prefix='/transaction',
    tags=[config.transaction_service.tags_metadata['name']],  # type: ignore
)
router.include_router(
    face_verification_router,
    prefix='/face_verification',
    tags=[config.face_verification.tags_metadata['name']],  # type: ignore
)
