from rest_framework import serializers
from .models import Import_Bill
from product.serializers import ProductSerializer

class ImportBillSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False,read_only=True)
    class Meta:
        model = Import_Bill
        fields = '__all__'