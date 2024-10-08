import pytest
from fastapi import status


@pytest.mark.anyio
async def test_registration(client, test_user, registration_link):
    """Registration test."""
    response = await client.post(registration_link, json=test_user)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()
    assert response.json()['token'] is not None


@pytest.mark.anyio
async def test_authentication(client, test_user, auth_link, registration_link):
    """Auth test."""
    await client.post(registration_link, json=test_user)
    response = await client.post(auth_link, json=test_user)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()
    assert response.json()['token'] is not None


@pytest.mark.anyio
async def test_registration_existing_user(
    client,
    test_user,
    registration_link,
):
    """Existing user registration test."""
    response = await client.post(registration_link, json=test_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()
    assert response.json()['detail'] is not None


@pytest.mark.anyio
async def test_wrong_login(
    auth_link,
    client,
    registration_link,
    wrong_user_data,
    test_user,
):
    """Auth test with incorrect data."""
    await client.post(registration_link, json=test_user)
    response = await client.post(auth_link, json=wrong_user_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'detail' in response.json()
    assert response.json()['detail'] is not None
