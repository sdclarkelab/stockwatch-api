from django.conf import settings
from django.db import models


class PortfolioStatus(models.Model):
    status_name = models.TextField(max_length=20)


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio_user')
    status = models.ForeignKey(PortfolioStatus, on_delete=models.CASCADE, related_name='portfolio_status')
    name = models.TextField(max_length=20, default="My Portfolio")
