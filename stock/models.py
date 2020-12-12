from django.db import models


class Stock(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='portfolio_stock')
    symbol = models.TextField(max_length=10)
    last_updated_date = models.DateTimeField(auto_now_add=True, null=True)
    is_archived = models.BooleanField(default=False)
    created_date = models.DateTimeField(null=True)


class StockCalculatedDetail(models.Model):
    symbol = models.TextField(max_length=10)
    total_shares = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    avg_net_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    current_value = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    total_net_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
