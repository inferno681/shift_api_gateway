from contextlib import asynccontextmanager
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)

import uvicorn
from fastapi import FastAPI, Request

from app.api import service_router
from config import config
from jaeger_client import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    tracer_config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'localhost',
                'reporting_port': '6831',
            },
            'logging': True,
        },
        service_name='gateway',
        validate=True,
    )
    tracer = tracer_config.initialize_tracer()
    app.state.jaeger_tracer = tracer
    yield
    tracer.close()


tags_metadata = [
    config.auth_service.tags_metadata,  # type: ignore
    config.transaction_service.tags_metadata,  # type: ignore
]


app = FastAPI(
    lifespan=lifespan,
    title=config.service.title,  # type: ignore
    description=config.service.description,  # type: ignore
    openapi_tags=tags_metadata,
    debug=config.service.debug,  # type: ignore
)  # type: ignore

app.include_router(service_router, prefix='/api')


@app.middleware("http")
async def tracing_middleware(request: Request, call_next):
    path = request.url.path
    if (
        path.startswith('/up')
        or path.startswith('/ready')
        or path.startswith('/metrics')
    ):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS, request.headers
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: str(request.url),
    }
    with global_tracer().start_active_span(
        f"gateway_{request.method}_{path}",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        response = await call_next(request)
        scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        return response


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=config.service.host,  # type: ignore
        port=config.service.port,  # type: ignore
    )  # noqa:WPS432
