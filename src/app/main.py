from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from jaeger_client import Config
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)

from app.api import service_router
from app.service import AuthServiceClient
from config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Запуск и остановка трейсера перед запуском приложения."""
    tracer_config = Config(
        config={
            'sampler': {
                'type': config.jaeger.sampler_type,  # type: ignore
                'param': config.jaeger.sampler_param,  # type: ignore
            },
            'local_agent': {
                'reporting_host': config.jaeger.host,  # type: ignore
                'reporting_port': config.jaeger.port,  # type: ignore
            },
            'logging': config.jaeger.logging,  # type: ignore
        },
        service_name=config.jaeger.service_name,  # type: ignore
        validate=True,
    )
    tracer = tracer_config.initialize_tracer()
    app.state.jaeger_tracer = tracer
    auth_client = AuthServiceClient(config.auth_service.base_url)  # type: ignore # noqa: E501
    app.state.auth_client = auth_client
    yield
    if tracer:
        tracer.close()
    await auth_client.aclose()


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


@app.middleware('http')
async def tracing_middleware(request: Request, call_next):
    """Middleware для трейсинга."""
    path = request.url.path
    if path.endswith(('/ready', '/metrics', '/docs', '/openapi.json')):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS,
            dict(request.headers),
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: str(request.url),
    }
    with global_tracer().start_active_span(
        f'gateway_{request.method}_{path}',
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
