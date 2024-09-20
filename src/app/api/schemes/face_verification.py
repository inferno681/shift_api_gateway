from pydantic import BaseModel, PositiveInt


class FaceVerificationRequest(BaseModel):
    """Схема запроса для формирования вектора."""

    link: str


class FaceVerificationResponse(FaceVerificationRequest):
    """Схема ответа с вектором."""

    user_id: PositiveInt
    embedding: list[float]
