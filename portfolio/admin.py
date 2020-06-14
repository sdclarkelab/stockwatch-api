from django.contrib import admin

from .models import Portfolio, StockStatus


class MyPortfolio(admin.ModelAdmin):
    list_display = ('id', 'name', 'status_id', 'user_id')


class MyStockStatus(admin.ModelAdmin):
    list_display = ('id', 'status_name')


admin.site.register(Portfolio, MyPortfolio)
admin.site.register(StockStatus, MyStockStatus)
