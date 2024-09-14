from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Errors scheme."""

    detail: str


class IsReady(BaseModel):
    """Health check response scheme."""

    is_ready: bool
