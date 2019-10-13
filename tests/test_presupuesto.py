import pytest
import json
from base.models import Presupuesto


request = {
    "date": "2019-10-25",
    "discount":"10",
    "items": [{"id":"1","quantity":"2"},{"id":"2","quantity":"1"}]
    }

request2 = {
    "date":"2019-10-19",
    "client":1,
    "items":[1],
    "discount":"10.00",
    # "total_before_discounts":"0.00",
    # "total_after_discounts":"0.00",
    # "total_iva":"0.00",
    "item":[{"product":1,"quantity":2}]
    #         {"presupuesto":81,"product":2,"quantity":1,"price":"99.00","iva":"20.79","final_price":"119.79"}]
    }
# eljason = json.dumps(request)

@pytest.mark.django_db(transaction=True)
def test_presupuesto_correct_result(django_client):
    response = django_client.post('/presupuesto/create/', request, format='json')
    # post(path, data=None, content_type=MULTIPART_CONTENT, follow=False, secure=False, **extra)
    # import pdb; pdb.set_trace()
    test = Presupuesto.objects.get(id=response.data['id'])
    assert test.total_after_discounts == 230.22


@pytest.mark.django_db(transaction=True)
def test_get(django_client):
    response = django_client.get('/presupuesto/')
    # import pdb; pdb.set_trace()
    assert response.status_code == 200

#TODO: encontrar la manera correcta de pasarle los items

# #un presupuesto ya hecho
# i=Presupuesto.objects.get(id=81)
# (Pdb) i
# <Presupuesto: 2019-10-18>
# (Pdb) i.item_set.all()
# <QuerySet [<Item: Item object (90)>, <Item: Item object (91)>]>
# (Pdb) i.item_set.first()
# <Item: Item object (90)>
# (Pdb) i.item_set.first().quantity
# 2

# #un presupuesto al que se le paso el request y el request2
# > c:\users\rocio\programacion\mafalda_proj\base\views.py(45)create()
# -> products_list = json.loads(post.get('items')) #json.loads transforma la lista en formato string a formato lista de python
# (Pdb) post
# <QueryDict: {}>
# (Pdb) presupuesto.id
# 89
# (Pdb) post
# <QueryDict: {}>
# (Pdb) self.request.POST
# <QueryDict: {}>
# (Pdb) json.loads(presupuesto.items)
# *** TypeError: the JSON object must be str, bytes or bytearray, not 'ManyRelatedManager'
# (Pdb)
# *** TypeError: the JSON object must be str, bytes or bytearray, not 'ManyRelatedManager'
# (Pdb) json.loads(presupuesto.item_set)
# *** TypeError: the JSON object must be str, bytes or bytearray, not 'RelatedManager'
# (Pdb) json.loads(presupuesto.item_set.all())
# *** TypeError: the JSON object must be str, bytes or bytearray, not 'QuerySet'
# (Pdb) json.loads(presupuesto.item_set.first())
# *** TypeError: the JSON object must be str, bytes or bytearray, not 'NoneType'
# (Pdb) o= presupuesto.item_set.first()
# (Pdb) o
# (Pdb) print(o)
# None
# (Pdb) presupuesto
# <Presupuesto: 2019-10-19>
# (Pdb) presupuesto.items
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x000001CCBD356438>
# (Pdb) presupuesto.items.all()
# <QuerySet []>
# (Pdb) presupuesto.client_id
# 1
# (Pdb) presupuesto.item_set.all()
# <QuerySet []>

