from django.urls import path, include
from . import views

urlpatterns = [

    #  -------------------------------------
    #             USER
    #  -------------------------------------
    path('', views.new_investor, name='new_investor'),
    path('get_id/', views.get_investor_id, name='get_investor_id'),
    path('<int:investor_id>/', views.investor_profile, name='investor_profile'),
    path('<int:investor_id>/portfolio/', include('portfolio.urls'))
]
