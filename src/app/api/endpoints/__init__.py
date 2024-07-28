from fastapi import APIRouter

from src.app.api.endpoints.auth import router as auth_router
from src.app.api.endpoints.transaction import router as transaction_router
from src.app.api.endpoints.face_verification import (
    router as face_verification_router,
)
from src.config import config

router = APIRouter()

router.include_router(
    auth_router,
    prefix='/auth',
    tags=[config.auth_service.tags_metadata['name']],
)
router.include_router(
    transaction_router,
    prefix='/transaction',
    tags=[config.transaction_service.tags_metadata['name']],
)
router.include_router(
    face_verification_router,
    prefix='/face_verification',
    tags=[config.face_verification.tags_metadata['name']],
)
