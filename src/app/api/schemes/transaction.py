from datetime import datetime
from enum import Enum

from pydantic import BaseModel, PositiveFloat, PositiveInt


class TransactionType(str, Enum):
    """Transaction types."""

    DEBIT = 'debit'
    CREDIT = 'credit'


class TransactionCreate(BaseModel):
    """Transaction creation scheme."""

    amount: PositiveInt | PositiveFloat
    transaction_type: TransactionType


class Transaction(TransactionCreate):
    """Transaction scheme."""

    user_id: PositiveInt
    id: PositiveInt
    created_at: datetime


class TransactionReportCreate(BaseModel):
    """Report creation scheme."""

    start_date: datetime
    end_date: datetime


class TransactionReport(TransactionReportCreate):
    """Report scheme."""

    user_id: PositiveInt
    transactions: list[TransactionType] | list
    debit: int
    credit: int
