import pytest
from fastapi import status


@pytest.mark.anyio
async def test_health_services(
    check_health_link,
    client,
    mock_get_health,
):
    """Health check test."""
    response = await client.get(check_health_link)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['is_ready'] is True


@pytest.mark.anyio
async def test_unhealth_services(
    check_health_link,
    client,
    mock_get_unhealth,
):
    """Health check with negative response."""
    response = await client.get(check_health_link)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert 'detail' in response.json()
