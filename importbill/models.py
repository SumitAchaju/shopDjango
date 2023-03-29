from django.db import models
from product.models import Product

class Import_Bill(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount_in_kg = models.FloatField(null=True,blank=True)
    amount_in_pcs = models.IntegerField()
    total_price = models.FloatField()
    discount_percentage = models.FloatField()
    discount_rate = models.FloatField()
    rate = models.FloatField()
    our_rate = models.FloatField()
    import_date = models.DateField()


    def __str__(self):
        return f"{self.import_date}"