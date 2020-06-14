from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('weights', views.stocks_weights, name='stocks_weights'),
    path('<str:symbol>/', views.stock_detail, name='stock_detail'),

    #  -------------------------------------
    #               TRANSACTION
    #  -------------------------------------
    path('<str:symbol>/transaction/', include('transaction.urls')),

    # #  -------------------------------------
    # #               NOTIFICATION
    # #  -------------------------------------
    # path('<str:symbol>/notification/', include('notification.urls')),
    #
    #  -------------------------------------
    #               PLAN
    #  -------------------------------------
    path('<str:symbol>/plan/', include('plan.urls')),

]
