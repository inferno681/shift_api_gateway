import pytest

from app.constants import (
    INVALID_INT_FLOAT_MESSAGE,
    INVALID_INT_MESSAGE,
    INVALID_TRANSACTION_TYPE_MESSAGE,
    WRONG_AMOUNT_MESSAGE,
    WRONG_ID_MESSAGE,
)
from app.service import TransactionType, report_storage, transaction_storage

USER_ID = 1
WRONG_VALUE = 'str'


@pytest.fixture(autouse=True)
def data_storage():
    """Фикстура для очистки хранилища перед каждым текстом."""
    transaction_storage.clear()
    report_storage.clear()
    yield
    transaction_storage.clear()
    report_storage.clear()


@pytest.fixture()
def debit_transaction():
    """Фикстура транзакции списания."""
    return {
        'user_id': USER_ID,
        'amount': 100,
        'transaction_type': TransactionType.DEBIT,
    }


@pytest.fixture()
def credit_transaction():
    """Фикстура транзакции пополнения."""
    return {
        'user_id': USER_ID,
        'amount': 200,
        'transaction_type': TransactionType.CREDIT,
    }


@pytest.fixture()
def transaction_data(request, debit_transaction, credit_transaction):
    """Фикстура подстановки транзакций списания и пополнения."""
    if request.param == 'debit':
        return debit_transaction
    elif request.param == 'credit':
        return credit_transaction
    else:
        raise ValueError(
            INVALID_TRANSACTION_TYPE_MESSAGE.format(value=request.param),
        )


@pytest.fixture(
    params=(
        {
            'data': {
                'user_id': WRONG_VALUE,
                'amount': 100,
                'transaction_type': TransactionType.DEBIT,
            },
            'error_message': INVALID_INT_MESSAGE.format(value=WRONG_VALUE),
        },
        {
            'data': {
                'user_id': -1,
                'amount': 100,
                'transaction_type': TransactionType.DEBIT,
            },
            'error_message': WRONG_ID_MESSAGE,
        },
        {
            'data': {
                'user_id': 123,
                'amount': -100,
                'transaction_type': TransactionType.DEBIT,
            },
            'error_message': WRONG_AMOUNT_MESSAGE,
        },
        {
            'data': {
                'user_id': 123,
                'amount': WRONG_VALUE,
                'transaction_type': TransactionType.DEBIT,
            },
            'error_message': INVALID_INT_FLOAT_MESSAGE.format(
                value=WRONG_VALUE,
            ),
        },
        {
            'data': {
                'user_id': 123,
                'amount': 100,
                'transaction_type': WRONG_VALUE,
            },
            'error_message': INVALID_TRANSACTION_TYPE_MESSAGE.format(
                value=WRONG_VALUE,
            ),
        },
    ),
    ids=(
        'wrong_id',
        'negative_id',
        'negative_amount',
        'wrong_amount',
        'wrong_transaction_type',
    ),
)
def invalid_transaction_data(request):
    """Фикстура с некорректными транзакциями."""
    return request.param
