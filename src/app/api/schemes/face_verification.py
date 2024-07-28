from pydantic import BaseModel, PositiveInt


class FaceVerificationRequest(BaseModel):
    """Схема запроса для формирования вектора."""

    user_id: PositiveInt
    link: str


class FaceVerificationResponse(FaceVerificationRequest):
    """Схема ответа с вектором."""

    embedding: list[float]
