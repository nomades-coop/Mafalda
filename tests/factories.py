import factory
from base.models import Product

class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product
    name = 'Pepe'
    title = 'El pepe de la gente'
    product_code = 'el pepe'
    wholesaler_code = '123456'
    iibb = '1234567891592'
    list_price= 90
    surcharge = 10
    iva_percentage = 21
    # company_id = 1
