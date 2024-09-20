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
def mock_post_registration_failure(httpx_mock):
    """Registration failure mock."""
    httpx_mock.add_response(
        method='POST',
        url=config.auth_service.base_url + REGISTRATION_LINK,
        json={'detail': 'error_message'},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@pytest.fixture
def mock_post_wrong_user_data(httpx_mock):
    """Auth failure mock."""
    httpx_mock.add_response(
        method='POST',
        url=config.auth_service.base_url + AUTH_LINK,
        json={'detail': 'error_message'},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def add_mock_response(httpx_mock, link: str) -> None:
    """Auth service response mock."""
    httpx_mock.add_response(
        method='POST',
        url=config.auth_service.base_url + link,  # type: ignore
        json={'token': 'token'},
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def reg_auth_links(request, registration_link, auth_link, httpx_mock):
    """Registration and auth responses mock."""
    if request.param == 'registration':
        add_mock_response(httpx_mock, REGISTRATION_LINK)
        return registration_link
    elif request.param == 'auth':
        add_mock_response(httpx_mock, AUTH_LINK)
        return auth_link


@pytest.fixture()
def transaction_data(
    request,
    debit_transaction,
    credit_transaction,
    httpx_mock,
):
    """Transaction creation response mock."""
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
def mock_post_check_token(httpx_mock):
    """Token check mock."""
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
def mock_post_create_report(httpx_mock):
    """Report creation response mock."""
    httpx_mock.add_response(
        method='POST',
        url=config.transaction_service.base_url + CREATE_REPORT_LINK,
        json={
            'user_id': 1,
            'start_date': 'string',
            'end_date': 'string',
            'transactions': [
                {
                    'id': 0,
                    'user_id': 0,
                    'amount': 'string',
                    'transaction_type': 'debit',
                    'created_at': 'string',
                },
            ],
            'debit': 'string',
            'credit': 'string',
        },
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def mock_post_create_wrong_report(httpx_mock):
    """Report creation with wrong data response mock."""
    httpx_mock.add_response(
        method='POST',
        url=config.transaction_service.base_url + CREATE_REPORT_LINK,
        json={'detail': 'some_error'},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@pytest.fixture
def mock_get_health(httpx_mock):
    """Health check positive response mock."""
    httpx_mock.add_response(
        method='GET',
        url=re.compile(rf'.*{re.escape(HEALTH_LINK)}$'),
        json={'is_ready': True},
        status_code=status.HTTP_200_OK,
    )


@pytest.fixture
def mock_get_unhealth(httpx_mock):
    """Health check negative response mock."""
    httpx_mock.add_response(
        method='GET',
        url=re.compile(rf'.*{re.escape(HEALTH_LINK)}$'),
        json={'detail': 'detail'},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
