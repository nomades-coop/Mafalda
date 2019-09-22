# from django.test import TestCase

# from .models import Product


# class ModelTestCase(TestCase):
#     """This class defines the test suite for the product model."""

#     def setUp(self):
#         """Define the test client and other test variables."""
#         self.product_name = "lapiz"
#         self.title= 'titulo'
#         self.code ='a1'
#         self.wcode ='a1'
#         self.iibb = 12345678912
#         self.lprice = 90
#         self.surcharge= 10
#         self.price = 0
#         self.iperc = 21
#         self.iva = 0
#         self.fprice = 0
#         self.product = Product(name=self.product_name, title= self.title,
#         product_code=self.code, wholesaler_code=self.wcode, iibb=self.iibb,
#         list_price=self.lprice, surcharge=self.surcharge, price=self.price,
#         iva_percentage=self.iperc, iva=self.iva, final_price=self.fprice,
#         picture=None)

#     def test_model_can_create_a_product(self):
#         """Test the product model can create a product."""
#         old_count = Product.objects.count()
#         self.product.save()
#         new_count = Product.objects.count()
#         self.assertNotEqual(old_count, new_count)
