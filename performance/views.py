from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import stock.services as stock_services
from services import jamstockex_api_service


@api_view(['GET'])
@protected_resource()
def performance_list(request, investor_id, portfolio_id):
    try:
        if request.method == 'GET':
            response = []
            stock_totals = stock_services.get_stock_totals()

            if stock_totals:
                stock_index_data_list = jamstockex_api_service.get_stocks_infos()
                response = stock_services.create_stock_performance_response(stock_totals, stock_index_data_list)

            return Response(response)
    except Exception as e:
        print(e)
        return Response({"message": "Error fetching performance list."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@protected_resource()
def performance_detail(request, investor_id, portfolio_id, symbol):
    """
    Retrieve Stock performance information
    """
    if request.method == 'GET':
        stock_detail = stock_services.get_stock_calculated_detail(investor_id, portfolio_id, symbol)
        return Response(stock_detail)
