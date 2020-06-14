from django.contrib import admin

from .models import Stock


class MyStock(admin.ModelAdmin):
    list_display = ('id', 'portfolio_id', 'symbol')


admin.site.register(Stock, MyStock)
