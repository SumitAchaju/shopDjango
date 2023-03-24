from rest_framework import viewsets, status
from .models import Import_Bill
from .serializers import ImportBillSerializer, ProductSerializer
from rest_framework.response import Response
from .utils.parse_importbillviewset_data import parse_data
from product.models import Product


class ImportBillViewSet(viewsets.ModelViewSet):
    queryset = Import_Bill.objects.all().order_by('-import_date')
    serializer_class = ImportBillSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        # Calulating required data and formating it in required form
        product_and_bill = parse_data(data)
        product_data = product_and_bill["product_data"]
        bill_data = product_and_bill["bill_data"]

        # Checking if Product already exists or not
        is_product_exists = Product.objects.filter(product_name=data['productName'])
        if is_product_exists:
            product_serializer = ProductSerializer(is_product_exists[0],data=product_data)
        else:
            product_serializer = ProductSerializer(data=product_data)
        
        # First saving the nested Product Instance
        if product_serializer.is_valid():
            product_instance = product_serializer.save()

            # Saving Bill Instance
            serializer = self.get_serializer(data=bill_data)
            if serializer.is_valid():
                bill_instance = serializer.save(product=product_instance)

                # Storing the latest bill id to product instance
                product_instance.latest_bill_id = bill_instance.id
                product_instance.save()
                
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, *args, **kwargs):
        return 
