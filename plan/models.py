from django.db import models


class Plan(models.Model):
    stock = models.OneToOneField('stock.Stock', on_delete=models.CASCADE, related_name='stock_plan')
    target_sell_price = models.DecimalField(decimal_places=2, max_digits=10)
