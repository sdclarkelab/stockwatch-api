from django.db import models


class Stock(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='portfolio_stock')
    symbol = models.TextField(max_length=10)

    class Meta:
        unique_together = (('portfolio', 'symbol'),)
