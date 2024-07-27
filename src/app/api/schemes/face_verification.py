from pydantic import BaseModel


class FaceVerificationRequest(BaseModel):
    """Схема запроса для формирования вектора."""

    link: str


class FaceVerificationResponse(FaceVerificationRequest):
    """Схема ответа с вектором."""

    embedding: list[float]
