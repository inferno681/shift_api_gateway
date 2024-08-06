import pytest
from datetime import datetime, timedelta, UTC
from httpx import ASGITransport, AsyncClient
import asyncio

from app.main import app


@pytest.fixture
def anyio_backend():
    """Бэкэнд для тестирования."""
    return 'asyncio'


@pytest.fixture
async def client():
    """Фикстура клиента для подключения к тестовому серверу."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://127.0.0.1:8000/api/',
    ) as client:
        yield client


@pytest.fixture
def registration_link():
    """Фикстура со ссылкой на регистрацию."""
    return '/auth/registration'


@pytest.fixture
def auth_link():
    """Фикстура со ссылкой на аутентификацию."""
    return '/auth/auth'


@pytest.fixture
def test_user():
    """Фикстура с данными пользователя."""
    return {'login': 'user', 'password': 'password'}


@pytest.fixture(
    params=(
        {'login': 'user', 'password': 'wrongpassword'},
        {'login': 'no_user', 'password': 'wrongpassword'},
    ),
    ids=('wrong_password', 'no_user'),
)
def wrong_user_data(request):
    """Фикстура с некорректными данными пользователя."""
    return request.param


@pytest.fixture()
def debit_transaction():
    """Фикстура транзакции списания."""
    return {
        'amount': 100,
        'transaction_type': 'списание',
    }


@pytest.fixture()
def credit_transaction():
    """Фикстура транзакции пополнения."""
    return {
        'amount': 200,
        'transaction_type': 'пополнение',
    }


@pytest.fixture()
def transaction_data(request, debit_transaction, credit_transaction):
    """Фикстура подстановки транзакций списания и пополнения."""
    if request.param == 'debit':
        return debit_transaction
    elif request.param == 'credit':
        return credit_transaction


@pytest.fixture
def create_transaction_link():
    """Ссылка на создание транзакции."""
    return '/transaction/create_transaction'


@pytest.fixture
def create_report_link():
    """Ссылка на создание отчета."""
    return '/transaction/create_report'


@pytest.fixture
def report_data():
    """Данные для запроса отчета."""
    return {
        'start_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
    }


@pytest.fixture
def wrong_report_data():
    """Некорректные данные для запроса отчета."""
    return {
        'start_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
    }


@pytest.fixture
def token(client, auth_link, test_user):
    """Токен существуюшего пользователя."""
    response = asyncio.run(client.post(auth_link, json=test_user))
    return response.json()['token']


@pytest.fixture
def face_embedding_link():
    """Ссылка на формирование эмбеддинга."""
    return '/face_verification/face_embedding'


@pytest.fixture()
def one_face_data():
    """Фикстура с корректным изображением."""
    return {'link': 'src/tests/images/one_face.jpg'}


@pytest.fixture()
def many_faces_data():
    """Фикстура с некорректным изображением."""
    return {'link': 'src/tests/images/many_faces.jpg'}
