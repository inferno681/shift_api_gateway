import pytest
from fastapi import status


@pytest.mark.anyio
@pytest.mark.parametrize(
    'reg_auth_links',
    [
        pytest.param('registration', id='registration'),
        pytest.param('auth', id='auth'),
    ],
    indirect=True,
)
async def test_registration_success(
    client,
    test_user,
    reg_auth_links,
):
    """Registration and auth test."""
    response = await client.post(url=reg_auth_links, json=test_user)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'token': 'token'}


@pytest.mark.anyio
async def test_registration_existing_user(
    client,
    test_user,
    mock_post_registration_failure,
    registration_link,
):
    """Existing user registration test."""
    await client.post(registration_link, json=test_user)
    response = await client.post(registration_link, json=test_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()


@pytest.mark.anyio
async def test_wrong_login(
    auth_link,
    client,
    wrong_user_data,
    mock_post_wrong_user_data,
):
    """Auth test with incorrect data."""
    response = await client.post(auth_link, json=wrong_user_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'detail' in response.json()
