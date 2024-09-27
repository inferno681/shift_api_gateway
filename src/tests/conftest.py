from datetime import UTC, datetime, timedelta

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(scope='session')
def anyio_backend():
    """Backend for test."""
    return 'asyncio'


@pytest.fixture(scope='session')
async def client():
    """Client for testing."""
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://127.0.0.1:8000/api/',
        ) as client:
            yield client


@pytest.fixture(scope='session')
def registration_link():
    """Registration link."""
    return '/auth/registration'


@pytest.fixture(scope='session')
def auth_link():
    """Auth link."""
    return '/auth/auth'


@pytest.fixture(scope='session')
def test_user():
    """User test data."""
    return {'login': 'user', 'password': 'password'}


@pytest.fixture(
    scope='session',
    params=(
        {'login': 'user', 'password': 'wrongpassword'},
        {'login': 'no_user', 'password': 'wrongpassword'},
    ),
    ids=('wrong_password', 'no_user'),
)
def wrong_user_data(request):
    """Incorrect user data."""
    return request.param


@pytest.fixture(scope='session')
def debit_transaction():
    """Debit transaction."""
    return {
        'amount': 100,
        'transaction_type': 'debit',
    }


@pytest.fixture(scope='session')
def credit_transaction():
    """Credit transaction."""
    return {
        'amount': 200,
        'transaction_type': 'credit',
    }


@pytest.fixture(scope='session')
def create_transaction_link():
    """Transaction creation link."""
    return '/transaction/create_transaction'


@pytest.fixture(scope='session')
def create_report_link():
    """Report creation link."""
    return '/transaction/create_report'


@pytest.fixture(scope='session')
def report_data():
    """Report request data."""
    return {
        'start_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
    }


@pytest.fixture(scope='session')
def wrong_report_data():
    """Incorrect request data."""
    return {
        'start_date': (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        'end_date': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
    }


@pytest.fixture(scope='session')
def check_health_link():
    """Health check link."""
    return '/healthz/ready'


@pytest.fixture(scope='session')
def verify_link():
    """Photo upload link."""
    return '/auth/verify'
