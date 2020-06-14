from django.contrib import admin

from .models import Transaction


class MyTransactions(admin.ModelAdmin):
    list_display = ('id', 'action', 'price', 'stock_symbol')

    def stock_symbol(self, obj):
        return obj.stock.symbol


admin.site.register(Transaction, MyTransactions)
