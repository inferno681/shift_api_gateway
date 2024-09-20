from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Схема для вывода ошибок."""

    detail: str
