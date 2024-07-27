import uvicorn
from fastapi import FastAPI

from src.app.api import router
from src.config import config

app = FastAPI(debug=config.service.debug)  # type: ignore

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=config.service.host,  # type: ignore
        port=config.service.port,  # type: ignore
    )  # noqa:WPS432
