import pytest
from django.test import Client

@pytest.fixture(scope='module')
def django_client():
    c = Client()
    yield c