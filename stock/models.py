from django.db import models


class Stock(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='portfolio_stock')
    symbol = models.TextField(max_length=50)
    is_archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)


class StockCalculatedDetail(models.Model):
    symbol = models.TextField(max_length=10)
    total_shares = models.DecimalField(decimal_places=10, max_digits=30, default=0.0)
    avg_net_price = models.DecimalField(decimal_places=10, max_digits=30, default=0.0)
    current_value = models.DecimalField(decimal_places=10, max_digits=30, default=0.0)
    total_net_amount = models.DecimalField(decimal_places=10, max_digits=30, default=0.0)
