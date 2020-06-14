from django.db import models


class Notification(models.Model):
    stock = models.OneToOneField('stock.Stock', on_delete=models.CASCADE, related_name='stock_notification')
    dividend_notification = models.BooleanField(default=False)
    sell_notification = models.BooleanField(default=False)
    sell_percentage_threshold = models.IntegerField(default=20)
