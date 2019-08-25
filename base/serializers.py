
from rest_framework import serializers
from .models import Company, Parameters, Product, Client, Presupuesto, Employee

class CompanySerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Company
        fields = ('id', 'name', 'razon_social', 'commercial_address', 'iibb', 'iva_condition', 'cuit', 'activity_start_date')

class ParametersSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Parameters
        fields = ('id', 'surcharge')

class ProductSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Product
        fields = ('id', 'name', 'title', 'product_code', 'wholesaler_code', 'iibb', 'iva', 'list_price', 'surcharge', 'company_id', 'picture')

class ClientSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Client
        fields = ('id', 'name_bussiness_name', 'commercial_address', 'cuit', 'iva_condition', 'sale_condition', 'company_id')

class PresupuestoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Presupuesto
        fields = ('id', 'date', 'products', 'price', 'iva', 'discounts')

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Employee
        fields = ('id', 'user', 'company_id')
