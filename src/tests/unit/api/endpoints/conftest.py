from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient, Response

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
def mock_client():
    """Фикстура для мока AsyncClient."""
    with patch('app.service.service.AsyncClient') as mock_client:
        yield mock_client


@pytest.fixture
def registration_link():
    """Фикстура со ссылкой на регистрацию."""
    return '/auth/registration'


@pytest.fixture
def auth_link():
    """Фикстура со ссылкой на аутентификацию."""
    return '/auth/auth'


@pytest.fixture
def mock_post_registration_success():
    """Фикстура для мока регистрации и авторизации."""
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_200_OK,
        json={'token': 'token'},
    )
    return mock_post


@pytest.fixture
def mock_post_registration_failure():
    """Фикстура для мока регистрации и авторизации."""
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_400_BAD_REQUEST,
        json={'detail': 'error_message'},
    )
    return mock_post


@pytest.fixture
def mock_post_wrong_user_data():
    """Фикстура для мока регистрации и авторизации."""
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_404_NOT_FOUND,
        json={'detail': 'error_message'},
    )
    return mock_post


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
def reg_auth_links(request, registration_link, auth_link):
    """Фикстура подстановки ссылок на регистрацию и авторизацию."""
    if request.param == 'registration':
        return registration_link
    elif request.param == 'auth':
        return auth_link


@pytest.fixture()
def debit_transaction():
    """Фикстура транзакции списания."""
    return {
        'user_id': 1,
        'amount': 100,
        'transaction_type': 'списание',
    }


@pytest.fixture()
def credit_transaction():
    """Фикстура транзакции пополнения."""
    return {
        'user_id': 1,
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
        'user_id': 1,
        'start_date': '2024-08-05T01:15:01.231Z',
        'end_date': '2024-08-05T01:15:01.231Z',
    }


@pytest.fixture
def wrong_report_data():
    """Некорректные данные для запроса отчета."""
    return {
        'user_id': 1,
        'start_date': '2024-08-05T01:15:01.231Z',
        'end_date': '2024-08-05T01:15:01.231Z',
    }


@pytest.fixture
def mock_post_transaction_create():
    """
    Фикстура для мока создания транзакции.

    Первые два ключа являются ответом на проверку токена.
    """
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_200_OK,
        json={
            'user_id': 1,
            'is_token_valid': True,
            'id': 1,
            'amount': 'string',
            'transaction_type': 'списание',
            'created_at': '2024-08-05T01:09:59.652Z',
        },
    )
    return mock_post


@pytest.fixture
def mock_post_create_report():
    """
    Фикстура для мока создания отчета.

    Первые два ключа являются ответом на проверку токена.
    """
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_200_OK,
        json={
            'user_id': 1,
            'is_token_valid': True,
            'start_date': '2024-08-05T01:15:01.231Z',
            'end_date': '2024-08-05T01:15:01.231Z',
            'transactions': [
                {
                    'id': 0,
                    'user_id': 0,
                    'amount': 'string',
                    'transaction_type': 'списание',
                    'created_at': '2024-08-05T01:15:01.231Z',
                },
            ],
            'debit': 'string',
            'credit': 'string',
        },
    )
    return mock_post


@pytest.fixture
def mock_post_create_wrong_report():
    """
    Фикстура для мока создания отчета.

    Первые два ключа являются ответом на проверку токена.
    """
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_400_BAD_REQUEST,
        json={'user_id': 1, 'is_token_valid': True, 'detail': 'some_error'},
    )
    return mock_post


@pytest.fixture
def face_embedding_link():
    """Ссылка на формирование эмбеддинга."""
    return '/face_verification/face_embedding'


@pytest.fixture()
def one_face_data():
    """Фикстура с корректным изображением."""
    return {'user_id': 1, 'link': 'src/tests/images/one_face.jpg'}


@pytest.fixture()
def many_faces_data():
    """Фикстура с некорректным изображением."""
    return {'user_id': 1, 'link': 'src/tests/images/many_faces.jpg'}


@pytest.fixture
def mock_post_one_face_response(one_face_data):
    """
    Фикстура для мока эмбеддингов.

    Первые два ключа являются ответом на проверку токена.
    """
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_200_OK,
        json={
            'user_id': 1,
            'is_token_valid': True,
            'link': one_face_data['link'],
            'embedding': [],
        },
    )
    return mock_post


@pytest.fixture
def mock_post_many_faces_response():
    """
    Фикстура для мока ответа для некорректного изображения.

    Первые два ключа являются ответом на проверку токена.
    """
    mock_post = AsyncMock()
    mock_post.return_value = Response(
        status.HTTP_400_BAD_REQUEST,
        json={'user_id': 1, 'is_token_valid': True, 'detail': 'some_error'},
    )
    return mock_post
