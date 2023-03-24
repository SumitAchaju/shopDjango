from django.db import models
import datetime

choice_sale_unit = [
    ("Pcs", "Pcs"),
    ("Kg", "Kg"),
    ("Dozn", "Dozn"),
    ("6Pcs", "6Pcs"),
]

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    in_stock = models.IntegerField()
    sales_unit = models.CharField(
        max_length=20, choices=choice_sale_unit, default="Pcs")
    rate = models.FloatField(default=0)
    our_rate = models.FloatField(default=0)
    discount_percentage = models.FloatField(default=0)
    discount_rate = models.FloatField(default=0)
    increment_percentage = models.FloatField(default=0)
    increment_rate = models.FloatField(default=0)
    latest_bill_date = models.DateField(default=datetime.date.today)
    latest_bill_id = models.IntegerField(default=1)

