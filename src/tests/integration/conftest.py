from datetime import datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from app.constants import CREDIT, DEBIT, INVALID_TRANSACTION_TYPE_MESSAGE
from app.main import app
from app.service import report_storage, transaction_storage
from tests.unit.service.conftest import USER_ID


@pytest.fixture
def anyio_backend():
    """Бэкэнд для тестирования."""
    return 'asyncio'


@pytest.fixture(autouse=True)
def data_storage():
    """Фикстура для очистки хранилища перед каждым текстом."""
    transaction_storage.clear()
    report_storage.clear()
    yield
    transaction_storage.clear()
    report_storage.clear()


@pytest.fixture
async def client():
    """Фикстура клиента."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://127.0.0.1:8000/',
    ) as client:
        yield client


@pytest.fixture()
def debit_transaction():
    """Фикстура транзакции списания."""
    return {
        'user_id': USER_ID,
        'amount': 100,
        'transaction_type': DEBIT,
    }


@pytest.fixture()
def credit_transaction():
    """Фикстура транзакции пополнения."""
    return {
        'user_id': USER_ID,
        'amount': 200,
        'transaction_type': CREDIT,
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


@pytest.fixture
def create_transaction_link():
    """Ссылка на создание транзакции."""
    return '/create_transaction'


@pytest.fixture
def create_report_link():
    """Ссылка на создание отчета."""
    return '/create_report'


@pytest.fixture
def report_data():
    """Данные для запроса отчета."""
    return {
        'user_id': USER_ID,
        'start_date': (datetime.now() - timedelta(days=1)).isoformat(),
        'end_date': (datetime.now() + timedelta(days=1)).isoformat(),
    }
