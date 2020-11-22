from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.create_stock_and_transaction, name='create_stock_and_transaction'),
    ]
