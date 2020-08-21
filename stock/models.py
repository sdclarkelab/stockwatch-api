from django.db import models


class StockStatus(models.Model):
    status_name = models.TextField(max_length=20)


class Stock(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='portfolio_stock')
    symbol = models.TextField(max_length=10)
    status = models.ForeignKey(StockStatus, on_delete=models.CASCADE, related_name='stock_status', null=True)

    class Meta:
        unique_together = (('portfolio', 'symbol'),)


class StockCalculatedDetail(models.Model):
    symbol = models.TextField(max_length=10)
    total_shares = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    total_net_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    avg_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    total_value = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
