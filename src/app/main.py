from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.api import service_router
from config import config

tags_metadata = [
    config.auth_service.tags_metadata,  # type: ignore
    config.transaction_service.tags_metadata,  # type: ignore
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Проверка сервисов перед запуском."""
    is_ready = False
    while not is_ready:
        async with AsyncClient() as client:
            response = await client.get('http://127.0.0.1/api//healthz/ready')
            if (
                response.status_code == status.HTTP_200_OK
                and response.json()['is_ready'] is True
            ):
                is_ready = True
    yield


app = FastAPI(
    lifespan=lifespan,
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
