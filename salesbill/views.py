from rest_framework import viewsets
from .models import Sales_Bill
from .serializers import SalesBillSerializer


class SalesBillViewSet(viewsets.ModelViewSet):
    queryset = Sales_Bill.objects.all().order_by('sales_date')
    serializer_class = SalesBillSerializer