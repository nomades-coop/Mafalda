import json
import decimal
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import (Parameters, Presupuesto, Product, Employee, Client, Company, Item)
from .serializers import (ParametersSerializer, PresupuestoSerializer, ProductSerializer,
                            EmployeeSerializer, ClientSerializer, CompanySerializer, ItemSerializer)


#PRESUPUESTO
#path()
class PresupuestoView(generics.ListAPIView):
    """Vista que muestra el queryset de los presupuestos"""
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer


def calculate_presupuesto(presupuesto, total_price, total_iva):
    presupuesto.total_iva = total_iva
    presupuesto.total_before_discounts = total_price
    presupuesto.discount = total_price*(float(presupuesto.discount)/100)
    presupuesto.total_after_discounts = total_price - presupuesto.discount
    presupuesto.total_after_discounts = total_price*(1-float(presupuesto.discount )/100)
    return presupuesto


#path()
class CreatePresupuestoView(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        id_presupuesto = serializer.instance.id
        presupuesto= Presupuesto.objects.get(id=id_presupuesto)
        post = self.request.POST
        # import pdb; pdb.set_trace()
        products_list = json.loads(post.get('items')) #json.loads transforma la lista en formato string a formato lista de python
        total_price = 0 #Lleva la cuenta del precio final a pagar por el cliente
        total_iva = 0
        item_in_memory = []

        for prod in products_list:
            product = Product.objects.get(id=prod['id'])
            surcharge_price = product.list_price*(1+product.surcharge/decimal.Decimal(100))
            iva= surcharge_price*(product.iva_percentage/decimal.Decimal(100))
            final_price = surcharge_price + iva
            # TODO: Instanciar sin guardar los items en una lista. bulk save. django debug toolbar.prefetch related
            item_in_memory.append(Item(presupuesto=serializer.instance,
                product=Product.objects.get(pk=prod['id']), quantity=prod['quantity'],
                price = surcharge_price, iva=iva, final_price=final_price))
            total_price += float(final_price)*float(prod['quantity'])
            total_iva += float(iva)*float(prod['quantity'])

        Item.objects.bulk_create(item_in_memory) #guarda en la base de datos todos los Item de una sola vez
        calculate_presupuesto(presupuesto, total_price, total_iva) #funcion definida mas arriba para sacar todos los calculos de esta funcion.
        presupuesto.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# #path()
# class CreatePresupuestoView(generics.ListCreateAPIView):
#     """Esta clase maneja los requests GET y POST."""
#     queryset = Presupuesto.objects.all()
#     serializer_class = PresupuestoSerializer

#     def perform_create(self, serializer):
#         """
#         View to create a new presupuesto. To create a new instance of the intermediate table Item,
#         this view initialize it in memory to save all together with bulk_create
#         """
#         serializer.save()
#         id_presupuesto = serializer.instance.id
#         presupuesto= Presupuesto.objects.get(id=id_presupuesto)
#         post = self.request.POST

#         products_list = json.loads(post.get('items')) #json.loads transforma la lista en formato string a formato lista de python
#         total_price = 0 #Lleva la cuenta del precio final a pagar por el cliente
#         total_iva = 0
#         item_in_memory = []

#         for prod in products_list:
#             product = Product.objects.get(id=prod['id'])
#             surcharge_price = product.list_price*(1+product.surcharge/decimal.Decimal(100))
#             iva= surcharge_price*(product.iva_percentage/decimal.Decimal(100))
#             final_price = surcharge_price + iva
#             # TODO: Instanciar sin guardar los items en una lista. bulk save. django debug toolbar.prefetch related
#             item_in_memory.append(Item(presupuesto=serializer.instance,
#                 product=Product.objects.get(pk=prod['id']), quantity=prod['quantity'],
#                 price = surcharge_price, iva=iva, final_price=final_price))
#             total_price += float(final_price)*float(prod['quantity'])
#             total_iva += float(iva)*float(prod['quantity'])

#         Item.objects.bulk_create(item_in_memory) #guarda en la base de datos todos los Item de una sola vez
#         calculate_presupuesto(presupuesto, total_price, total_iva) #funcion definida mas arriba para sacar todos los calculos de esta funcion.
#         presupuesto.save()



#path()
class DetailsPresupuestoView(generics.RetrieveUpdateDestroyAPIView):
    """Esta clase maneja los requests GET, PUT, PATCH y DELETE para el presupuesto elegido via id."""
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer


#COMPANY
#path()
class CompanyView(generics.ListAPIView):
    """Vista que muestra el queryset de la empresa"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

#path()
class CreateCompanyView(generics.ListCreateAPIView):
    """Esta clase maneja los requests GET y POST."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        """Guarda la información de la nueva empresa"""
        serializer.save()

#path()
class DetailsCompanyView(generics.RetrieveUpdateDestroyAPIView):
    """Esta clase maneja los requests GET, PUT, PATCH y DELETE ."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


#PARAMETERS
#path()
class ParametersView(generics.ListAPIView):
    """Vista que muestra el queryset de la empresa"""
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer

#path()
class CreateParametersView(generics.ListCreateAPIView):
    """Esta clase maneja los requests GET y POST."""
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer

    def perform_create(self, serializer):
        """Guarda la información de la nueva empresa"""
        serializer.save()

#path()
class DetailsParametersView(generics.RetrieveUpdateDestroyAPIView):
    """Esta clase maneja los requests GET, PUT, PATCH y DELETE ."""
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer

#PRODUCTS
# path('')
class ProductView(generics.ListAPIView):
    """Vista que muestra el queryset de los productos."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#path()
class CreateProductView(generics.ListCreateAPIView):
    """Esta clase maneja los requests GET y POST."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """Guarda la info al crear un nuevo producto."""
        serializer.save()

# decimal.Decimal(self.amount)
#path()
class DetailsProductView(generics.RetrieveUpdateDestroyAPIView):
    """Esta clase maneja los requests GET, PUT, PATCH y DELETE ."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#CLIENT
#path()
class ClientView(generics.ListAPIView):
    """Vista que muestra el queryset de los clientes."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

#path()
class CreateClientView(generics.ListCreateAPIView):
    """Esta clase maneja los requests GET y POST."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        """?"""
        serializer.save()

#path()
class DetailsClientView(generics.RetrieveUpdateDestroyAPIView):
    """Esta clase maneja los requests GET, PUT, PATCH y DELETE ."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer




#EMPLOYEE
#path()
class EmployeeView(generics.ListAPIView):
    """Vista que muestra el queryset de los empleados."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

#path()
class CreateEmployeeView(generics.ListCreateAPIView):
    """Esta clase maneja los requests GET y POST."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        """?"""
        serializer.save()

#path()
class DetailsEmployeeView(generics.RetrieveUpdateDestroyAPIView):
    """Esta clase maneja los requests GET, PUT, PATCH y DELETE ."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
