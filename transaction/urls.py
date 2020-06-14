from django.urls import path

from . import views

urlpatterns = [
    path('', views.add_transaction, name='add_transaction'),
    path('<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
]
