import pytest
import json
from base.models import Presupuesto, Product
from .factories import ProductFactory


request = {
    "date": "2019-10-25",
    "discount":"10",
    "items": '[{"id":"1","quantity":"2"},{"id":"2","quantity":"1"}]'
    }

record1 = {
    "name" : 'Pepe',
    "title" : 'El pepe de la gente',
    "product_code" : 'el pepe',
    "wholesaler_code" : '123456',
    "iibb" : '1234567891592',
    "list_price": 90,
    "surcharge" : 10,
    "iva_percentage" : 21
}
record2 = {
    "name" : 'Pepe2',
    "title" : 'El pepe de la gente',
    "product_code" : 'el pepe',
    "wholesaler_code" : '123456',
    "iibb" : '1234567891592',
    "list_price": 90,
    "surcharge" : 10,
    "iva_percentage" : 21
}


# @pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_post(django_client):
    # record1 = ProductFactory()
    post = django_client.post('/product/create/', record1, format='json')
    assert post.status_code == 201


# @pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_get(django_client,django_db_setup):
    response = django_client.get('/products/')
    assert response.status_code == 200
    assert len(response.json()) == 13


# @pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_presupuesto_correct_result(django_client,django_db_setup):
    response = django_client.post('/presupuesto/create/', request, format='json')
    assert response.status_code == 201
    test = Presupuesto.objects.get(id=response.data['id'])
    assert float(test.total_after_discounts) == 230.22


