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
        is_product_exists = Product.objects.filter(
            product_name=data['productName'])
        if is_product_exists:
            product_serializer = ProductSerializer(
                is_product_exists[0], data=product_data)
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

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        # Getting the required bill to be updated
        instance = self.get_object()
        product = Product.objects.filter(
            product_name=request.data["productName"])
        # Checking if user input product already exists or not if not returning the bad request
        if not product:
            print("not product")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # checking if the user input product is different than previous if it does, returning the bad request
        if product[0].id != instance.product.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Now calculating and formating the required data
        if request.data["discountType"] == "Rs":
            discount_rate = request.data["discount"]
            discount_percentage = discount_rate/100 * request.data["rate"]
        else:
            discount_percentage = request.data["discount"]
            discount_rate = discount_percentage * 100 / request.data["rate"]
        data = {
            "total_price": request.data["buy"],
            "amount_in_pcs": request.data["quantity"],
            "amount_in_kg": request.data["kg"],
            "rate": request.data["rate"],
            "our_rate": request.data["ourRate"],
            "import_date": request.data["date"],
            "discount_rate": discount_rate,
            "discount_percentage": discount_percentage
        }
        # checking if current bill is linked to latest product or not if it does changing the product data according to bill
        if product[0].latest_bill_id == instance.id:
            product_price = product[0].increment_rate + data["our_rate"]
            product_update_data = {
                "price": product_price,
                "rate": data["rate"],
                "our_rate": data["our_rate"],
                "discount_rate": discount_rate,
                "discount_percentage": discount_percentage,
                "latest_bill_date": data["import_date"]
            }
            product_serializer = ProductSerializer(
                product[0], data=product_update_data, partial=True)
            if product_serializer.is_valid():
                product_serializer.save()

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        new_serializer = self.get_serializer(self.get_object(), many=False)
        return Response(new_serializer.data, status=status.HTTP_200_OK)
