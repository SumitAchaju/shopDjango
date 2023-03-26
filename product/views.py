from rest_framework import viewsets,status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-latest_bill_date')
    serializer_class = ProductSerializer

    def partial_update(self, request, *args, **kwargs):
        show = request.data.pop("show")
        instance = self.get_object()
        if show == "%":
            increment_percentage = float(request.data.pop("increment"))
            increment_rate = (increment_percentage/100) * instance.our_rate
        else:
            increment_rate = float(request.data.pop("increment"))
            increment_percentage = (increment_rate*100) / instance.our_rate

        request.data["increment_percentage"] = increment_percentage
        request.data["increment_rate"] = increment_rate
        if int(request.data["in_stock"]) < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)
    