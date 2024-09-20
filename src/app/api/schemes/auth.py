from pydantic import BaseModel, Field, PositiveInt

from app.constants import KAFKA_RESPONSE


class UserCreate(BaseModel):
    """User registration scheme."""

    login: str = Field(
        description='Login',
        min_length=3,
        max_length=20,  # noqa:WPS432
        pattern='^[a-zA-Z0-9._-]+$',
    )
    password: str = Field(
        description='Password',
        min_length=6,
        max_length=100,
    )


class UserToken(BaseModel):
    """Token sending scheme."""

    token: str | None = None


class UserTokenCheck(BaseModel):
    """Token check scheme."""

    user_id: PositiveInt | None = None
    is_token_valid: bool


class KafkaResponse(BaseModel):
    """Photo sending response."""

    message: str = KAFKA_RESPONSE
