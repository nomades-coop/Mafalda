import json
import pytest

from django.contrib.auth.models import User
from base.models import Presupuesto, Client, Company, Employee


request = {
    "date": "2019-10-25",
    "discount":"10",
    "items": '[{"id":"1","quantity":"2"},{"id":"2","quantity":"1"}]'
    }

CLIENT_REQUEST = {
    "name_bussinessname": "Blancanieves",
    "commercial_address":"Pueyrredon 934",
    "cuit" : "12345678978",
    "iva_condition" : "Responsable inscripto",
    "company_id" : 1
    }

CLIENT_REQUEST_PUT = {
    "name_bussinessname": "Cenicienta",
    "commercial_address":"Pueyrredon 9343",
    "cuit" : "15345678978",
    "iva_condition" : "Responsable inscripto",
    "company_id" : 1
    }

CLIENT_REQUEST_PUT_BAD_INFO = {
    "name_bussinessname": 1,
    "commercial_address": 2,
    "cuit" : 3,
    "iva_condition" : 4,
    "company_id" : 1
    }

COMPANY_REQUEST = {
    "name": "Uber",
    "razon_social":"El Uber",
    "commercial_address": "Laminar 456",
    "iibb" : "1234567897894561230258746",
    "iva_condition" : "RIN",
    "cuit" : "12345678978",
    "activity_start_date" : "1986-10-25"
    }

COMPANY_REQUEST_PUT = {
    "name": "Google",
    "razon_social":"El -google",
    "commercial_address": "Laminar 456",
    "iibb" : "1234567897894561230258746",
    "iva_condition" : "RIN",
    "cuit" : "12345678979",
    "activity_start_date" : "1986-12-26"
    }

EMPLOYEE_REQUEST = {
    "user" : 3,
    "company_id": 1
    }

EMPLOYEE_REQUEST_PUT = {
    "user" : 1,
    "company_id": 1
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

# tests del endpoint /product/
@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_post_presupuesto(django_client):
    # record1 = ProductFactory()
    post = django_client.post('/product/', record1, format='json')
    assert post.status_code == 201


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_get_presupuesto(django_client, django_db_setup):
    response = django_client.get('/products/')
    assert response.status_code == 200
    assert len(response.json()) == 13


# tests del endpoint /presupuesto/
@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_presupuesto_correct_result(django_client, django_db_setup):
    response = django_client.post('/presupuesto/', request, format='json')
    assert response.status_code == 201
    test = Presupuesto.objects.get(id=response.data['id'])
    assert float(test.total_after_discounts) == 230.22


# tests del endpoint /client/
@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_get_list_of_clients(django_client, django_db_setup):
    response = django_client.get('/client/')
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_get_client_by_id(django_client, django_db_setup):
    response = django_client.get('/client/2/')
    assert response.status_code == 200


@pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_get_client_bad_id(django_client, django_db_setup):
    response = django_client.get('/client/pepe/')
    assert response.status_code == 404


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_post_new_client(django_client, django_db_setup):
    response = django_client.post('/client/', CLIENT_REQUEST, format='json')
    assert response.status_code == 201
    test = Client.objects.get(id=response.data['id'])
    assert test.name_bussinessname == 'Blancanieves'


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_put_client(django_client, django_db_setup):
    response = django_client.put('/client/2/', CLIENT_REQUEST_PUT, format='json')
    assert response.status_code == 200
    test = Client.objects.get(id=response.data['id'])
    assert test.name_bussinessname == 'Cenicienta'

#TODO: hacer validaciones para crear un nuevo cliente?
@pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_put_client_bad_info(django_client, django_db_setup):
    response = django_client.put('/client/2/', CLIENT_REQUEST_PUT_BAD_INFO, format='json')
    import pdb; pdb.set_trace()
    assert response.status_code == 200
    test = Client.objects.get(id=response.data['id'])
    assert test.name_bussinessname == 'Cenicienta'


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_patch_client(django_client, django_db_setup):
    response = django_client.patch('/client/2/', data={'name_bussinessname':'Elsa'}, format='json')
    assert response.status_code == 200
    test = Client.objects.get(id=response.data['id'])
    assert test.name_bussinessname == 'Elsa'


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_delete_client(django_client, django_db_setup):
    response = django_client.delete('/client/2/')
    assert response.status_code == 204


# tests del endpoint /company/
@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_get_list_of_company(django_client, django_db_setup):
    response = django_client.get('/company/')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_get_company_by_id(django_client, django_db_setup):
    response = django_client.get('/company/1/')
    assert response.status_code == 200


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_get_company_bad_id(django_client, django_db_setup):
    response = django_client.get('/company/pepe/')
    assert response.status_code == 404


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_post_new_company(django_client, django_db_setup):
    response = django_client.post('/company/', COMPANY_REQUEST, format='json')
    assert response.status_code == 201
    test = Company.objects.get(id=response.data['id'])
    assert test.name == 'Uber'


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_put_company(django_client, django_db_setup):
    response = django_client.put('/company/1/', COMPANY_REQUEST_PUT, format='json')
    assert response.status_code == 200
    test = Company.objects.get(id=response.data['id'])
    assert test.name == 'Google'


@pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_put_company_bad_info(django_client, django_db_setup):
    response = django_client.put('/company/1/', CLIENT_REQUEST_PUT_BAD_INFO, format='json')
    import pdb; pdb.set_trace()
    assert response.status_code == 200
    test = Company.objects.get(id=response.data['id'])
    assert test.name_bussinessname == 'Cenicienta'


@pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_patch_company(django_client, django_db_setup):
    response = django_client.patch('/company/1/', data={'name':'Rocio'}, format='json')
    assert response.status_code == 200
    test = Company.objects.get(id=response.data['id'])
    assert test.name_bussinessname == 'Rocio'


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_delete_company(django_client, django_db_setup):
    response = django_client.delete('/company/1/')
    assert response.status_code == 204


# tests del endpoint /employee/

@pytest.mark.django_db(transaction=True)
def test_get_list_of_employee(django_client, django_db_setup):
    response = django_client.get('/employee/')
    assert response.status_code == 200
    # assert len(response.json()) == 2


@pytest.mark.django_db(transaction=True)
def test_get_employee_by_id(django_client, django_db_setup):
    response = django_client.get('/employee/1/')
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_get_employee_bad_id(django_client, django_db_setup):
    response = django_client.get('/employee/pepe/')
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_post_new_employee(django_client, django_db_setup):
    User.objects.create_user('test', email= None, password='testpassword')
    response = django_client.post('/employee/', EMPLOYEE_REQUEST, format='json')
    assert response.status_code == 201



@pytest.mark.django_db(transaction=True)
def test_put_employee(django_client, django_db_setup):
    response = django_client.put('/employee/2/', EMPLOYEE_REQUEST_PUT, format='json')
    assert response.status_code == 400
    assert response.json() == {'user': ['This field must be unique.']}


@pytest.mark.skip("WIP")
@pytest.mark.django_db(transaction=True)
def test_patch_employeey(django_client, django_db_setup):
    response = django_client.patch('/employee/2/', data={'user':'Federico'}, format='json')
    assert response.status_code == 200
    test = Employee.objects.get(id=response.data['id'])
    assert test.name_bussinessname == 'Federico'



@pytest.mark.django_db(transaction=True)
def test_delete_employee(django_client, django_db_setup):
    response = django_client.delete('/employee/2/')
    assert response.status_code == 204