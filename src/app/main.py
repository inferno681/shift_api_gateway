import uvicorn
from fastapi import FastAPI

from app.api import service_router
from config import config

tags_metadata = [
    config.auth_service.tags_metadata,
    config.transaction_service.tags_metadata,
    config.face_verification.tags_metadata,
]

app = FastAPI(
    title=config.service.title,
    description=config.service.description,
    openapi_tags=tags_metadata,
    debug=config.service.debug,
)  # type: ignore

app.include_router(service_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=config.service.host,  # type: ignore
        port=config.service.port,  # type: ignore
    )  # noqa:WPS432
