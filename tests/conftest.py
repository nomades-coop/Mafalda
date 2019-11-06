import pytest
import json

from rest_framework.test import APIClient
from django.core.management import call_command
from django.contrib.auth.models import User


@pytest.fixture(scope='module')
@pytest.mark.django_db(transaction=True)
def django_client():
    user = User.objects.get(username='test')
    c= APIClient()
    c.force_authenticate(user=user)
    yield c

@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'company_data.json','products_data.json',
            'clients_data.json', 'company_data.json', 'employee_data.json',
            'user_data.json', 'parameters_data.json', 'presupuestos_data.json')
