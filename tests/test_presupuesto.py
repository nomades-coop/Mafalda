import pytest
import json

request = {"date": "2019-10-25", "discount":10, "items": [{"id":"1","quantity":"2"},{"id":"2","quantity":"1"}]}


@pytest.mark.django_db(transaction=True)
def test_presupuesto_correct_result(django_client):
    response = django_client.post('/presupuesto/create/', request)
    import pdb; pdb.set_trace()
    assert response.total_after_discounts == 230.22


@pytest.mark.django_db(transaction=True)
def test_get(django_client):
    response = django_client.get('/presupuesto/')
    assert response.status_code == 200
