from rest_framework import viewsets,status
from .models import Sales_Bill,Product
from .serializers import SalesBillSerializer
from rest_framework.response import Response


class SalesBillViewSet(viewsets.ModelViewSet):
    queryset = Sales_Bill.objects.all().order_by('-sales_date')
    serializer_class = SalesBillSerializer

    def create(self, request, *args, **kwargs):
        product_name = request.data.pop('product')
        product_instance = Product.objects.get(product_name=product_name)
        product_instance.in_stock -= request.data["pcs"] 
        product_instance=product_instance.save()
        bill_data = calculate(request.data,product_instance)
        serializer = self.get_serializer(data=bill_data)
        if serializer.is_valid():
            serializer.save(product=product_instance)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def calculate(data,product):
    pcs = data.pop("pcs")
    total_sales_price = data.pop("amount")
    our_rate = product.our_rate
    our_sales_price = product.price

    total_profit = total_sales_price - (our_rate*pcs)

    profit = total_profit / pcs

    discount_on_sales = our_sales_price - (total_sales_price / pcs)

    discount_percentage_on_sales = discount_on_sales * 100 / our_sales_price

    required_data = {
        "amount_in_pcs":pcs,
        "total_sales":total_sales_price,
        "total_profit":total_profit,
        "profit":profit,
        "discount_percentage":discount_percentage_on_sales,
        "discount_rate":discount_on_sales,
        "sales_date":data.pop("date")
    }

    return required_data
    