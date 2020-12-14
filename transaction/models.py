from django.db import models


class TransactionAction(models.Model):
    action = models.TextField(max_length=20)


class Transaction(models.Model):
    stock = models.ForeignKey('stock.Stock', on_delete=models.CASCADE, related_name='stock_transaction')
    action = models.ForeignKey(TransactionAction, on_delete=models.CASCADE, related_name='transaction_action',
                               null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    shares = models.IntegerField(default=0)
    fees = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    gross_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    net_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    net_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    last_updated_date = models.DateTimeField(auto_now_add=True, null=True)
