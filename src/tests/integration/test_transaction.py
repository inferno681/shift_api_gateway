import pytest
from fastapi import status


@pytest.mark.anyio
@pytest.mark.parametrize(
    'transaction_data',
    [
        pytest.param('credit', id='credit_transaction'),
        pytest.param('debit', id='debit_transaction'),
    ],
    indirect=True,
)
async def test_create_transaction(
    client,
    create_transaction_link,
    transaction_data,
    token,
):
    """Тест создания транзакции."""
    response = await client.post(
        create_transaction_link,
        json=transaction_data,
        headers={'Authorization': token},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert 'created_at' in response_data
    assert 'id' in response_data
    assert 'user_id' in response_data
    assert (
        response_data['transaction_type']
        == transaction_data['transaction_type']
    )
    assert response_data['amount'] == transaction_data['amount']


@pytest.mark.anyio
async def test_create_report(
    client,
    debit_transaction,
    credit_transaction,
    create_report_link,
    create_transaction_link,
    report_data,
    token,
):
    """Тест создания отчета."""
    await client.post(
        create_transaction_link,
        json=debit_transaction,
        headers={'Authorization': token},
    )
    await client.post(
        create_transaction_link,
        json=credit_transaction,
        headers={'Authorization': token},
    )
    response = await client.post(
        create_report_link,
        json=report_data,
        headers={'Authorization': token},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert isinstance(response_data['transactions'], list)


@pytest.mark.anyio
async def test_create_report_wrong_dates(
    client,
    debit_transaction,
    credit_transaction,
    create_report_link,
    create_transaction_link,
    wrong_report_data,
    token,
):
    """Тест создания отчета."""
    await client.post(
        create_transaction_link,
        json=debit_transaction,
        headers={'Authorization': token},
    )
    await client.post(
        create_transaction_link,
        json=credit_transaction,
        headers={'Authorization': token},
    )
    response = await client.post(
        create_report_link,
        json=wrong_report_data,
        headers={'Authorization': token},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()
    assert response.json()['detail'] is not None
