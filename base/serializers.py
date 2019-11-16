
from rest_framework import serializers
from .models import Company, Parameters, Product, Client, Presupuesto, Employee, Item

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
        fields = ('id', 'name', 'title', 'product_code', 'wholesaler_code', 'iibb', 'list_price', 'surcharge', 'company_id', 'picture', 'iva_percentage', 'final_price', 'active')

class ClientSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Client
        fields = ('id', 'name_bussinessname', 'commercial_address', 'cuit', 'iva_condition', 'sale_condition', 'company_id')

class ItemSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Item
        fields = ('presupuesto','product', 'quantity', 'price','iva', 'final_price')
        # depth = 2

class PresupuestoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    prod = ProductSerializer(many=True, read_only=True)
    item = ItemSerializer(many=True, read_only=True, source='item_set')

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Presupuesto
        fields = ('id', 'date', 'client', 'items', 'discount',
        'total_before_discounts', 'total_after_discounts', 'total_iva', 'prod', 'item')

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Employee
        fields = ('id', 'user', 'company_id')
