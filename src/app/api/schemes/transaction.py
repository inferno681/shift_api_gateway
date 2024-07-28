from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, PositiveFloat, PositiveInt


class TransactionType(str, Enum):
    """Типы транзакций."""

    DEBIT = 'списание'
    CREDIT = 'пополнение'


class TransactionCreate(BaseModel):
    """Схема создания транзакции."""

    amount: PositiveInt | PositiveFloat
    transaction_type: TransactionType


class Transaction(TransactionCreate):
    """Схема транзакции."""

    user_id: PositiveInt
    id: PositiveInt
    created_at: datetime


class TransactionReportCreate(BaseModel):
    """Схема создания отчета."""

    start_date: datetime
    end_date: datetime


class TransactionReport(TransactionReportCreate):
    """Схема отчета."""

    user_id: PositiveInt
    transactions: list[TransactionType] | list
    debit: Decimal
    credit: Decimal
