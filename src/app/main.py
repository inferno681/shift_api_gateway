import uvicorn
from fastapi import FastAPI

from app.api import service_router
from config import config

tags_metadata = [
    config.auth_service.tags_metadata,  # type: ignore
    config.transaction_service.tags_metadata,  # type: ignore
]

app = FastAPI(
    title=config.service.title,  # type: ignore
    description=config.service.description,  # type: ignore
    openapi_tags=tags_metadata,
    debug=config.service.debug,  # type: ignore
)  # type: ignore

app.include_router(service_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=config.service.host,  # type: ignore
        port=config.service.port,  # type: ignore
    )  # noqa:WPS432
