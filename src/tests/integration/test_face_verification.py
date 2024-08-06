import pytest
from fastapi import status


@pytest.mark.anyio
async def test_vector_generation(
    client,
    face_embedding_link,
    one_face_data,
    token,
):
    """Тест генерации вектора."""
    response = await client.post(
        face_embedding_link,
        json=one_face_data,
        headers={'Authorization': token},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert 'link' in response_data
    assert 'embedding' in response_data
    assert len(response_data['embedding']) == 128


@pytest.mark.anyio
async def test_many_faces_error(
    client,
    face_embedding_link,
    many_faces_data,
    token,
):
    """Тест исключения (несколько лиц на изображении)."""
    response = await client.post(
        face_embedding_link,
        json=many_faces_data,
        headers={'Authorization': token},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()
    assert response.json()['detail'] is not None
