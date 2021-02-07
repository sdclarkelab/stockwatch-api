from django.db import models


class PlanStatus(models.Model):
    status_name = models.TextField(max_length=20)


class Plan(models.Model):
    stock = models.OneToOneField('stock.Stock', on_delete=models.CASCADE, related_name='stock_plan')
    target_sell_price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.ForeignKey(PlanStatus, on_delete=models.CASCADE, related_name='plan_status', null=True)
