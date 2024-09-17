import pytest
from fastapi import status


@pytest.mark.anyio
async def test_check_healthz(client, check_health_link):
    """Health check test."""
    response = await client.get(check_health_link)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['is_ready'] is True
