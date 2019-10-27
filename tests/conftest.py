import pytest
import json
# from django.test import Client

# @pytest.fixture(scope='module')
# def django_client():
#     c = Client()
#     yield c

from rest_framework.test import APIClient
from django.core.management import call_command


@pytest.fixture(scope='module')
def django_client():
    c = APIClient()
    yield c

@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'company_data.json','products_data.json',
             'clients_data.json', 'company_data.json', 'employee_data.json', 'user_data.json')
