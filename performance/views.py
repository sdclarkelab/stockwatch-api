from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import stock.services as stock_services


@api_view(['GET'])
@protected_resource()
def performance_list(request, investor_id, portfolio_id):
    try:
        if request.method == 'GET':
            stock_dicts = stock_services.get_stocks_dicts(investor_id, portfolio_id)
            response = []
            for stocks in stock_dicts:
                stock_detail = stock_services.get_stock_calculated_detail(investor_id, portfolio_id, stocks['symbol'])
                if stock_detail:
                    response.append(stock_detail)

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
