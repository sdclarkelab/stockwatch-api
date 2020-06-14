from django.urls import path

from . import views

urlpatterns = [
    path('', views.new_notification, name='new_notification'),
    path('<int:notification_id>/', views.notification_detail, name='notification_detail'),
]
