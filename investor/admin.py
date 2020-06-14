from django.contrib import admin

from .models import Investor


class MyInvestor(admin.ModelAdmin):
    list_display = ('id', 'is_staff', 'ipo_notification')


admin.site.register(Investor, MyInvestor)
