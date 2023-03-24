from rest_framework import serializers
from .models import Sales_Bill
from product.serializers import ProductSerializer

class SalesBillSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False,read_only=True)
    class Meta:
        model = Sales_Bill
        fields = '__all__'