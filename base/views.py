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
def calculate_presupuesto(presupuesto, total_price, total_iva):
    presupuesto.total_iva = total_iva
    presupuesto.total_before_discounts = total_price
    presupuesto.discount = total_price*(float(presupuesto.discount)/100)
    presupuesto.total_after_discounts = total_price - presupuesto.discount
    presupuesto.total_after_discounts = total_price*(1-float(presupuesto.discount )/100)
    return presupuesto


class PresupuestoView(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        id_presupuesto = serializer.instance.id
        presupuesto= Presupuesto.objects.get(id=id_presupuesto)
        post = self.request.data
        products_list = json.loads(post.get('items')) #json.loads transforma la lista en formato string a formato lista de python
        total_price = 0 #Lleva la cuenta del precio final a pagar por el cliente
        total_iva = 0
        item_in_memory = []

        for prod in products_list:
            product = Product.objects.get(id=prod['id'])
            surcharge_price = product.list_price*(1+product.surcharge/decimal.Decimal(100))
            iva= surcharge_price*(product.iva_percentage/decimal.Decimal(100))
            final_price = surcharge_price + iva
            item_in_memory.append(Item(presupuesto=serializer.instance,
                product=Product.objects.get(pk=prod['id']), quantity=prod['quantity'],
                price = surcharge_price, iva=iva, final_price=final_price))
            total_price += float(final_price)*float(prod['quantity'])
            total_iva += float(iva)*float(prod['quantity'])

        Item.objects.bulk_create(item_in_memory) #guarda en la base de datos todos los Item de una sola vez
        calculate_presupuesto(presupuesto, total_price, total_iva) #funcion definida mas arriba para sacar todos los calculos de esta funcion.
        presupuesto.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#COMPANY
class CompanyView(viewsets.ModelViewSet):
    """Vista de la empresa Mafalda. OJO! Pueden crearse muchas empresas"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


#PARAMETERS
class ParametersView(viewsets.ModelViewSet):
    """
    Vista que muestra, crea y modifica el parámetro recargo que aplica
    la empresa por default a todos sus productos
    """
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer


#PRODUCTS
class ProductView(viewsets.ModelViewSet):
    """Vista para manejar los productos de la librería"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """Función que crea un nuevo producto"""
        serializer.save()
        id_product = serializer.instance.id
        product= Product.objects.get(id=id_product)
        if product.surcharge == 0:
            product.surcharge = Parameters.objects.get(id=1).surcharge
        product.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#CLIENT
class ClientView(viewsets.ModelViewSet):
    """
    Esta vista maneja los clientes de la empresa Mafalda,
    a quien se le hacen los presupuestos
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        """Función que crea un nuevo cliente"""
        serializer.save()


#EMPLOYEE
class EmployeeView(viewsets.ModelViewSet):
    """Esta vista maneja los empleados que hacen los presupuestos"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        """Función que crea un nuevo empleado"""
        serializer.save()
