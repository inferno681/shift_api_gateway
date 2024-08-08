from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Схема для вывода ошибок."""

    detail: str


class IsReady(BaseModel):
    """Схема ответа health check."""

    is_ready: bool
