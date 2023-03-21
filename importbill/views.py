from rest_framework import viewsets,status
from .models import Import_Bill
from .serializers import ImportBillSerializer,ProductSerializer
from rest_framework.response import Response


class ImportBillViewSet(viewsets.ModelViewSet):
    queryset = Import_Bill.objects.all().order_by('import_date')
    serializer_class = ImportBillSerializer

    def create(self, request, *args, **kwargs):
        product_data = request.data.pop('product')
        product_serializer = ProductSerializer(data=product_data)

        if product_serializer.is_valid():
            product_instance = product_serializer.save()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product_instance)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
