import re

import pytest
from fastapi import status

from app.constants import (
    AUTH_LINK,
    CHECK_TOKEN_LINK,
    CREATE_REPORT_LINK,
    CREATE_TRANSACTION_LINK,
    HEALTH_LINK,
    REGISTRATION_LINK,
)
from config import config


@pytest.fixture
def registration_link():
    """Фикстура со ссылкой на регистрацию."""
    return '/auth/registration'


@pytest.fixture
def auth_link():
    """Фикстура со ссылкой на аутентификацию."""
    return '/auth/auth'


@pytest.fixture
def mock_post_registration_failure(httpx_mock):
    """Фикстура для мока регистрации."""
    httpx_mock.add_response(
        method='POST',
        url=config.auth_service.base_url + REGISTRATION_LINK,
        json={'detail': 'error_message'},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@pytest.fixture
def mock_post_wrong_user_data(httpx_mock):
    """Фикстура для мока регистрации и авторизации."""
    httpx_mock.add_response(
        method='POST',
        url=config.auth_service.base_url + AUTH_LINK,
        json={'detail': 'error_message'},
        status_code=status.HTTP_404_NOT_FOUND,
    )


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


def add_mock_response(httpx_mock, link: str) -> None:
    """Добавляет мок для HTTP-запроса к сервису авторизации."""
    httpx_mock.add_response(
        method='POST',
        url=config.auth_service.base_url + link,  # type: ignore
        json={'token': 'token'},
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def reg_auth_links(request, registration_link, auth_link, httpx_mock):
    """Фикстура подстановки ссылок на регистрацию и авторизацию."""
    if request.param == 'registration':
        add_mock_response(httpx_mock, REGISTRATION_LINK)
        return registration_link
    elif request.param == 'auth':
        add_mock_response(httpx_mock, AUTH_LINK)
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
def transaction_data(
    request,
    debit_transaction,
    credit_transaction,
    httpx_mock,
):
    """Фикстура подстановки транзакций списания и пополнения."""
    if request.param == 'debit':
        debit_transaction_mock = debit_transaction.copy()
        debit_transaction_mock['id'] = 1
        debit_transaction_mock['user_id'] = 1
        debit_transaction_mock['created_at'] = '2024-08-05T01:09:59.652Z'
        httpx_mock.add_response(
            method='POST',
            url=config.transaction_service.base_url + CREATE_TRANSACTION_LINK,
            json=debit_transaction_mock,
            status_code=status.HTTP_200_OK,
        )
        return debit_transaction

    elif request.param == 'credit':
        credit_transaction_mock = credit_transaction.copy()
        credit_transaction_mock['id'] = 1
        credit_transaction_mock['user_id'] = 1
        credit_transaction_mock['created_at'] = '2024-08-05T01:09:59.652Z'
        httpx_mock.add_response(
            method='POST',
            url=config.transaction_service.base_url + CREATE_TRANSACTION_LINK,
            json=credit_transaction_mock,
            status_code=status.HTTP_200_OK,
        )
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
def mock_post_check_token(httpx_mock):
    """Фикстура для мока токена."""
    httpx_mock.add_response(
        method='POST',
        url=config.auth_service.base_url + CHECK_TOKEN_LINK,
        json={
            'user_id': 1,
            'is_token_valid': True,
        },
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def mock_post_transaction_create(httpx_mock):
    """Фикстура для мока создания транзакции."""
    httpx_mock.add_response(
        method='POST',
        url=config.transaction_service.base_url + CREATE_TRANSACTION_LINK,
        json={
            'id': 1,
            'amount': 'string',
            'transaction_type': 'списание',
            'created_at': '2024-08-05T01:09:59.652Z',
        },
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def mock_post_create_report(httpx_mock):
    """Фикстура для мока создания отчета."""
    httpx_mock.add_response(
        method='POST',
        url=config.transaction_service.base_url + CREATE_REPORT_LINK,
        json={
            'user_id': 1,
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
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def mock_post_create_wrong_report(httpx_mock):
    """Фикстура для мока создания отчета."""
    httpx_mock.add_response(
        method='POST',
        url=config.transaction_service.base_url + CREATE_REPORT_LINK,
        json={'detail': 'some_error'},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@pytest.fixture
def face_embedding_link():
    """Ссылка на формирование эмбеддинга."""
    return '/face_verification/face_embedding'


@pytest.fixture
def check_health_link():
    """Фикстура со ссылкой на проверку готовности сервиса."""
    return '/healthz/ready'


@pytest.fixture
def mock_get_health(httpx_mock):
    """Фикстура с положительным ответом о готовности сервисов."""
    httpx_mock.add_response(
        method='GET',
        url=re.compile(rf'.*{re.escape(HEALTH_LINK)}$'),
        json={'is_ready': True},
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def mock_get_unhealth(httpx_mock):
    """Фикстура с отрицательным ответом о готовности сервисов."""
    httpx_mock.add_response(
        method='GET',
        url=re.compile(rf'.*{re.escape(HEALTH_LINK)}$'),
        json={'detail': 'detail'},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


@pytest.fixture
def verify_link():
    """Фикстура со ссылкой для отправки фото."""
    return '/verify'
