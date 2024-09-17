import pytest


@pytest.fixture()
def transaction_data(request, debit_transaction, credit_transaction):
    """Transaction data based on the requested transaction type.."""
    if request.param == 'debit':
        return debit_transaction
    elif request.param == 'credit':
        return credit_transaction


@pytest.fixture
async def token(client, auth_link, test_user):
    """User token."""
    response = await client.post(auth_link, json=test_user)
    return response.json()['token']


@pytest.fixture()
def one_face_data():
    """Correct image."""
    return {'link': 'src/tests/images/one_face.jpg'}


@pytest.fixture()
def many_faces_data():
    """Incorrect image."""
    return {'link': 'src/tests/images/many_faces.jpg'}
