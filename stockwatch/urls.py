"""stockwatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import page_not_found
from stock import views as stock_views

urlpatterns = [
    path('api/v1/stockwatch_admin/', admin.site.urls),
    path('api/v1/stockwatch_admin/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/v1/investor/', include('investor.urls')),
    path('api/v1/stockNames/', stock_views.stock_names, name='stock_names'),

]

handler404 = page_not_found
handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'
