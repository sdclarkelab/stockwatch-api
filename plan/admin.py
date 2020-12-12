from django.contrib import admin

from .models import Plan


class MyPlan(admin.ModelAdmin):
    list_display = ('id', 'target_sell_price', 'status', 'sold_date')


admin.site.register(Plan, MyPlan)
