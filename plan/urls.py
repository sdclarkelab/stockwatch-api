from django.urls import path

from . import views

urlpatterns = [
    path('', views.plan, name='plan'),
    path('<int:plan_id>/', views.plan_detail, name='plan_detail'),
]
