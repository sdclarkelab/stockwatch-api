from django.db import models


class StockStatus(models.Model):
    status_name = models.TextField(max_length=20)


class Stock(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='portfolio_stock')
    symbol = models.TextField(max_length=10)
    status = models.ForeignKey(StockStatus, on_delete=models.CASCADE, related_name='stock_status', null=True)
    created_date = models.DateTimeField(null=True)
    sold_date = models.DateTimeField(null=True)


class StockCalculatedDetail(models.Model):
    symbol = models.TextField(max_length=10)
    total_shares = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    avg_net_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    current_value = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    total_net_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
