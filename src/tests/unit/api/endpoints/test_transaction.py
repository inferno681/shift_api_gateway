import pytest
from fastapi import status


@pytest.mark.anyio
@pytest.mark.parametrize(
    'transaction_data',
    [
        pytest.param('debit', id='debit_transaction'),
        pytest.param('credit', id='credit_transaction'),
    ],
    indirect=True,
)
async def test_create_transaction(
    client,
    create_transaction_link,
    transaction_data,
    mock_client,
    mock_post_transaction_create,
):
    """Тест создания транзакции."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_transaction_create
    )
    response = await client.post(
        create_transaction_link,
        json=transaction_data,
        headers={'Authorization': 'token'},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert 'created_at' in response_data
    assert 'id' in response_data
    assert 'user_id' in response_data
    assert 'amount' in response_data
    assert 'transaction_type' in response_data


@pytest.mark.anyio
async def test_create_report(
    client,
    create_report_link,
    report_data,
    mock_client,
    mock_post_create_report,
):
    """Тест создания отчета."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_create_report
    )
    response = await client.post(
        create_report_link,
        json=report_data,
        headers={'Authorization': 'token'},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data['transactions']) == 1
    assert 'user_id' in response_data
    assert 'start_date' in response_data
    assert 'end_date' in response_data
    assert 'debit' or 'credit' in response_data


@pytest.mark.anyio
async def test_create_report_wrong_dates(
    client,
    create_report_link,
    wrong_report_data,
    mock_client,
    mock_post_create_wrong_report,
):
    """Тест создания отчета."""
    mock_client.return_value.__aenter__.return_value.post = (
        mock_post_create_wrong_report
    )
    response = await client.post(
        create_report_link,
        json=wrong_report_data,
        headers={'Authorization': 'token'},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()
