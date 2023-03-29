from django.db import models
from product.models import Product

class Sales_Bill(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount_in_pcs = models.IntegerField()
    total_sales = models.FloatField()
    total_profit = models.FloatField()
    profit = models.FloatField(default=0)
    discount_percentage = models.FloatField()
    discount_rate = models.FloatField()
    sales_date = models.DateField()

    def __str__(self):
        return self.sales_date
