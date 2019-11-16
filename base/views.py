import os
import json
import decimal
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import (Parameters, Presupuesto, Product, Employee, Client,
                    Company, Item)
from .serializers import (ParametersSerializer, PresupuestoSerializer,
    ProductSerializer, EmployeeSerializer, ClientSerializer,
    CompanySerializer, ItemSerializer)
from rest_framework.authtoken.models import Token



def calculate_presupuesto(presupuesto, total_price, total_iva):
    presupuesto.total_iva = total_iva
    presupuesto.total_before_discounts = total_price
    presupuesto.discount = total_price*(float(presupuesto.discount)/100)
    presupuesto.total_after_discounts = total_price - presupuesto.discount
    presupuesto.total_after_discounts = total_price*(1-float(presupuesto.discount )/100)
    return presupuesto

def validar_cuit(cuit):
    # validaciones minimas
    if len(cuit) != 11 :
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    # calculo el digito verificador:
    aux = 0
    for i in range(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])


#PRESUPUESTO
class PresupuestoView(viewsets.ModelViewSet):
    """Vista para manejar los presupuestos de la librería"""
    serializer_class = PresupuestoSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Trae solo los activos y los de la compañia del usuario logueado
        cambiar el registro en urls: router.register(r'product', ProductView, basename='Product')
        """
        return Presupuesto.objects.filter(company_id=self.request.user.employee.company.id, active=True)


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
            surcharge_price = product.list_price*(
                1+product.surcharge/decimal.Decimal(100))
            iva= surcharge_price*(product.iva_percentage/decimal.Decimal(100))
            final_price = surcharge_price + iva
            item_in_memory.append(Item(presupuesto=serializer.instance,
                product=Product.objects.get(pk=prod['id']),
                quantity=prod['quantity'], price = surcharge_price, iva=iva,
                final_price=final_price))
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
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Función que crea una nueva compania"""
        serializer.save()
        id_company= serializer.instance.id
        company = Company.objects.get(id=id_company)
        cuit = company.cuit
        iibb=company.iibb
        valid_iibb = validar_cuit(iibb)
        valid_cuit = validar_cuit(cuit)
        if valid_cuit or valid_iibb != True:
            raise ValueError('El cuit ingresado no es válido.')


#PARAMETERS
class ParametersView(viewsets.ModelViewSet):
    """
    Vista que muestra, crea y modifica el parámetro recargo que aplica
    la empresa por default a todos sus productos
    """
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer
    # permission_classes = (permissions.IsAuthenticated,)


#PRODUCTS
class ProductView(viewsets.ModelViewSet):
    """Vista para manejar los productos de la librería"""
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Trae solo los activos y los de la compañia del usuario logueado
        cambiar el registro en urls: router.register(r'product', ProductView, basename='Product')
        """
        return Product.objects.filter(company_id=self.request.user.employee.company.id, active=True)


    def perform_create(self, serializer):
        """Función que crea un nuevo producto"""
        # company_id = Token.objects.get(key=request.auth.key).user.employee.company.id
        serializer.save()
        id_product = serializer.instance.id
        product= Product.objects.get(id=id_product)
        # user = Token.objects.get(key=self.request.auth.key).user
        # print(user.username, user.company_id)
        if product.surcharge == 0:
            product.surcharge = Parameters.objects.get(id=1).surcharge
        surcharge_price = product.list_price*(
                1+product.surcharge/decimal.Decimal(100))
        iva= surcharge_price*(product.iva_percentage/decimal.Decimal(100))
        product.final_price = surcharge_price + iva
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
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Función que crea un nuevo cliente"""
        serializer.save()
        id_client= serializer.instance.id
        client = Client.objects.get(id=id_client)
        cuit = client.cuit
        valid = validar_cuit(cuit)
        if valid != True:
            raise ValueError('El cuit ingresado no es válido.')


#EMPLOYEE
class EmployeeView(viewsets.ModelViewSet):
    """Esta vista maneja los empleados que hacen los presupuestos"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Función que crea un nuevo empleado"""
        serializer.save()
