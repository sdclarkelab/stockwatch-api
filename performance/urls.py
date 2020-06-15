from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.performance_list, name='performance_list'),
    path('stock/<str:symbol>/', views.performance_detail, name='performance_detail'),
]