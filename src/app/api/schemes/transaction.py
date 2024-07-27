from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, PositiveFloat, PositiveInt


class TransactionCreate(BaseModel):
    """Схема создания транзакции."""

    amount: PositiveInt | PositiveFloat
    transaction_type: str


class Transaction(TransactionCreate):
    """Схема транзакции."""

    user_id: PositiveInt
    id: PositiveInt
    created_at: datetime


class TransactionReportCreate(BaseModel):
    """Схема создания отчета."""

    user_id: PositiveInt
    start_date: datetime
    end_date: datetime


class TransactionReport(TransactionReportCreate):
    """Схема отчета."""

    transactions: list
    debit: Decimal
    credit: Decimal
