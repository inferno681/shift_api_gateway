import pytest
from fastapi import status


@pytest.mark.anyio
async def test_vector_generation(
    client,
    face_embedding_link,
    one_face_data,
    mock_post_one_face_response,
    mock_client,
):
    """Тест генерации вектора."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_one_face_response
    )
    response = await client.post(
        face_embedding_link,
        json=one_face_data,
        headers={'Authorization': 'token'},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert 'link' in response_data
    assert 'embedding' in response_data
    assert isinstance(response_data['embedding'], list)


@pytest.mark.anyio
async def test_many_faces_error(
    client,
    face_embedding_link,
    many_faces_data,
    mock_client,
    mock_post_many_faces_response,
):
    """Тест исключения (несколько лиц на изображении)."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_many_faces_response
    )
    response = await client.post(
        face_embedding_link,
        json=many_faces_data,
        headers={'Authorization': 'token'},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()
