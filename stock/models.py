from django.db import models


class StockStatus(models.Model):
    status_name = models.TextField(max_length=20)


class Stock(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='portfolio_stock')
    symbol = models.TextField(max_length=10)
    status = models.ForeignKey(StockStatus, on_delete=models.CASCADE, related_name='stock_status', null=True)

    class Meta:
        unique_together = (('portfolio', 'symbol'),)
