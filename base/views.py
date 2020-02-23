import os
import json
import decimal
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.views.decorators.csrf import csrf_exempt

from .models import (Parameters, Presupuesto, Product, Employee, Client,
                     Company, Item)
from .serializers import (ParametersSerializer, PresupuestoSerializer,
                          ProductSerializer, EmployeeSerializer, ClientSerializer,
                          CompanySerializer, ItemSerializer)

from rest_framework.authtoken.models import Token


development = os.environ['MAFALDA_ENV']


class MyCustomException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


def calculate_presupuesto(presupuesto, total_price, total_iva):
    presupuesto.total_iva = total_iva
    presupuesto.total_before_discounts = total_price
    presupuesto.discount = total_price*(float(presupuesto.discount)/100)
    presupuesto.total_after_discounts = total_price - presupuesto.discount
    presupuesto.total_after_discounts = total_price * \
        (1-float(presupuesto.discount)/100)
    return presupuesto


# PRESUPUESTO
class PresupuestoView(viewsets.ModelViewSet):
    """Vista para manejar los presupuestos de la librería"""
    serializer_class = PresupuestoSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Trae solo los activos y los de la compañia del usuario logueado
        cambiar el registro en urls: router.register(r'product', ProductView, basename='Product')
        """
        if development == 'development':
            return Presupuesto.objects.filter(active=True)
        else:
            return Presupuesto.objects.filter(company_id=self.request.user.employee.company.id, active=True)

    def perform_create(self, serializer):
        """Función que crea un nuevo presupuesto"""
        if development == 'development':
            if self.request.user.is_anonymous == True:
                owner = User.objects.get(id=1)
                company = Company.objects.get(id=1)
                serializer.save(owner=owner, company=company)
        else:
            owner = self.request.user
            company = self.request.user.employee.company
            serializer.save(company=company, owner=owner)

        id_presupuesto = serializer.instance.id
        presupuesto = Presupuesto.objects.get(id=id_presupuesto)
        post = self.request.data
        # json.loads transforma la lista en formato string a formato lista de python
        products_list = json.loads(post.get('items'))
        total_price = 0  # Lleva la cuenta del precio final a pagar por el cliente
        total_iva = 0
        item_in_memory = []

        for prod in products_list:
            product = Product.objects.get(id=prod['id'])
            surcharge_price = product.list_price*(
                1+product.surcharge/decimal.Decimal(100))
            iva = surcharge_price*(product.iva_percentage/decimal.Decimal(100))
            final_price = surcharge_price + iva
            item_in_memory.append(Item(presupuesto=serializer.instance,
                                       product=Product.objects.get(
                                           pk=prod['id']),
                                       quantity=prod['quantity'], price=surcharge_price, iva=iva,
                                       final_price=final_price))
            total_price += float(final_price)*float(prod['quantity'])
            total_iva += float(iva)*float(prod['quantity'])

        # guarda en la base de datos todos los Item de una sola vez
        Item.objects.bulk_create(item_in_memory)
        # funcion definida mas arriba para sacar todos los calculos de esta funcion.
        calculate_presupuesto(presupuesto, total_price, total_iva)
        presupuesto.active = True
        presupuesto.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Función que elimina un Presupuesto"""
        presupuesto = Presupuesto.objects.get(id=pk)
        presupuesto.active = False
        presupuesto.save()
        return Response({'Mensaje':'Presupuesto borrado'}, status=status.HTTP_200_OK)


# PARAMETERS
class ParametersView(viewsets.ModelViewSet):
    """
    Vista que muestra, crea y modifica el parámetro recargo que aplica
    la empresa por default a todos sus productos
    """
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer
    # permission_classes = (permissions.IsAuthenticated,)


# PRODUCTS
class ProductView(viewsets.ModelViewSet):
    """Vista para manejar los productos de la librería"""
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # TODO: el company decadaproducto se tiene que grabar automaticamente segun el usuario logueado

    def get_queryset(self):
        """
        Trae solo los activos y los de la compañia del usuario logueado
        cambiar el registro en urls: router.register(r'product', ProductView, basename='Product')
        """
        # para que traiga todo.development
        if development == 'development':
            return Product.objects.filter(active=True)
        else:
            return Product.objects.filter(company_id=self.request.user.employee.company.id, active=True)

    def perform_create(self, serializer):
        """Función que crea un nuevo producto"""
        if development == 'development'and self.request.user.is_anonymous == True:
                owner = User.objects.get(id=1)
                company = Company.objects.get(id=1)
                #serializer.save(owner=owner, company=company)
        else:
            owner = self.request.user
            company = self.request.user.employee.company
            #serializer.save(company=company, owner=owner)

        serializer.save(owner=owner, company=company)
        
        id_product = serializer.instance.id
        product = Product.objects.get(id=id_product)
        # user = Token.objects.get(key=self.request.auth.key).user
        # print(user.username, user.company_id)
        if product.surcharge == 0:
            product.surcharge = Parameters.objects.get(id=1).surcharge
        surcharge_price = product.list_price*(
            1+product.surcharge/decimal.Decimal(100))
        iva = surcharge_price*(product.iva_percentage/decimal.Decimal(100))
        product.final_price = surcharge_price + iva
        product.active = True
        product.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    
    def destroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.active = False
        product.save()
        return Response({'Mensaje':'Producto borrado'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def drop_auth_token(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    return Response(
        {"Mensaje": "Usuario aniquilado"},
        status=status.HTTP_200_OK
    )

@csrf_exempt
# @api_view(('POST',))
def search_view(request):
    text_search = json.loads(request.POST['text'])
    results = Product.objects.filter(
        Q(name__icontains=text_search) | Q(
            title__icontains=text_search) | Q(brand__icontains=text_search)
    )
    # results = Product.objects.filter(
    #     Q(name__icontains=text_search)
    # )
    result_list = []
    # for result in results:
    #     name = result.name
    #     result_list.append(name)

    for result in results:
        name = result.name
        brand = result.brand
        title = result.title
        result_dict = dict(name=name, brand=brand, title=title)
        result_list.append(result_dict)

    return JsonResponse({"Products": result_list})


# CLIENT
class ClientView(viewsets.ModelViewSet):
    """
    Esta vista maneja los clientes de la empresa Mafalda, a quien se le hacen los presupuestos.
    """
    serializer_class = ClientSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Trae solo los clientes de la compañia del usuario logueado
        cambiar el registro en urls, por ejemplo: router.register(r'product', ProductView, basename='Product')
        """
        if development == 'development':
            return Client.objects.filter(active=True)
        else:
            return Client.objects.filter(company_id=self.request.user.employee.company.id, active=True)


    def perform_create(self, serializer):
        """Función que crea un nuevo cliente"""
        print (development)
        print (self.request.user.employee.company)
        if development == 'development'and self.request.user.is_anonymous == True:
                owner = User.objects.get(id=1)
                company = Company.objects.get(id=1)
                #serializer.save(owner=owner, company=company)
                
        else:
            owner = self.request.user
            company = self.request.user.employee.company
            #serializer.save(company=company, owner=owner)

        serializer.save(company=company, owner=owner)
        id_client = serializer.instance.id
        client = Client.objects.get(id=id_client)
        client.active= True
        client.save()
            # id_client= serializer.instance.id
            # client = Client.objects.get(id=id_client)
            # cuit = client.cuit
            # valid = validar_cuit(cuit)
            # if valid == False:
            #     raise MyCustomExcpetion(detail={"Causa": "El cuit ingresado no es válido"}, status_code=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def destroy(self, request, pk=None):
        client = Client.objects.get(id=pk)
        client.active = False
        client.save()



# # EMPLOYEE
# class EmployeeView(viewsets.ModelViewSet):
#     """Esta vista maneja los empleados que hacen los presupuestos"""
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     # permission_classes = (permissions.IsAuthenticated,)

#     def perform_create(self, serializer):
#         """Función que crea un nuevo empleado"""
#         serializer.save()

#     def destroy(self, request, pk=None):
#         """Función que elimina un empleado"""
#         employee = Employee.objects.get(id=pk)
#         employee.active = False
#         employee.save()
#         return Response({'Mensaje':'Empleado borrado'}, status=status.HTTP_200_OK)


# # COMPANY
# class CompanyView(viewsets.ModelViewSet):
#     """Vista de la empresa Mafalda. OJO! Pueden crearse muchas empresas"""
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     # permission_classes = (permissions.IsAuthenticated,)

#     def perform_create(self, serializer):
#         """Función que crea una nueva compania"""
#         serializer.save()
#         id_company = serializer.instance.id
#         company = Company.objects.get(id=id_company)
#         cuit = company.cuit
#         iibb = company.iibb
#         valid_iibb = validar_cuit(iibb)
#         valid_cuit = validar_cuit(cuit)
#         # TODO: ver el raise este como en cliente
#         if valid_cuit or valid_iibb != True:
#             raise ValueError('El cuit ingresado no es válido.')
    
#     def destroy(self, request, pk=None):
#         """Función que elimina una Compañia"""
#         company = Company.objects.get(id=pk)
#         company.active = False
#         company.save()
#         return Response({'Mensaje':'Compañia borrado'}, status=status.HTTP_200_OK)

