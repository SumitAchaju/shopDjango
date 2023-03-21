from rest_framework import serializers
from .models import Sales_Bill

class SalesBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales_Bill
        fields = '__all__'