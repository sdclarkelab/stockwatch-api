from django.urls import path, include

from . import views

#  TODO: Show 404 is incorrect url is entered. Check django setting for Debug mode
urlpatterns = [
    #  -------------------------------------
    #               PORTFOLIO
    #  -------------------------------------
    path('', views.portfolio_list, name='portfolio_list'),
    path('<int:portfolio_id>/', views.portfolio_detail, name='portfolio_detail'),

    #  -------------------------------------
    #               STOCK
    #  -------------------------------------
    path('<int:portfolio_id>/stock/', include('stock.urls')),

    #  -------------------------------------
    #               PERFORMANCE
    #  -------------------------------------
    path('<int:portfolio_id>/performance/', include('performance.urls')),

    #  -------------------------------------
    #               IMPORTERS
    #  -------------------------------------
    path('<int:portfolio_id>/import/', include('importer.urls')),

    #  -------------------------------------
    #               STOCK_TRANSACTION
    #  -------------------------------------
    path('<int:portfolio_id>/stock_transaction', include('stock_transaction.urls'))
]
