from django.urls import path

from . import views

urlpatterns = [
    path('jmmb', views.jmmb_importer, name='jmmb_importer'),
]
