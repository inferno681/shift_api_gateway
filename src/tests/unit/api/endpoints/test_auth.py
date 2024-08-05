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
    mock_client,
    mock_post_registration_success,
    reg_auth_links,
):
    """Тест успешной регистрации и авторизации."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_registration_success
    )

    response = await client.post(url=reg_auth_links, json=test_user)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'token': 'token'}


@pytest.mark.anyio
async def test_registration_existing_user(
    client,
    test_user,
    mock_client,
    mock_post_registration_failure,
    registration_link,
):
    """Тест регистрации уже существующего пользователя."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_registration_failure
    )
    await client.post(registration_link, json=test_user)
    response = await client.post(registration_link, json=test_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()


@pytest.mark.anyio
async def test_wrong_login(
    auth_link,
    client,
    wrong_user_data,
    mock_client,
    mock_post_wrong_user_data,
):
    """Тест аутентификации пользователя с некорректными данными."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_wrong_user_data
    )
    response = await client.post(auth_link, json=wrong_user_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'detail' in response.json()
