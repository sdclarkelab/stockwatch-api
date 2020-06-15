from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
import stock.services as stock_services
from services import jamstockex_api_service
from utils.custom_json_resp import CustomJsonResponse
from .serializers import StockSerializer


@api_view(['GET', 'DELETE'])
@protected_resource()
def stock_detail(request, investor_id, portfolio_id, symbol):
    """
    Retrieve or delete a stock.
    """
    if request.method == 'GET':
        stock_detail_dict = stock_services.get_stock_detail_dict(investor_id, portfolio_id, symbol)
        return Response(stock_detail_dict)

    elif request.method == 'DELETE':
        stock = stock_services.get_stock_serializer(investor_id, portfolio_id, symbol)
        stock.delete()
        return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@protected_resource()
def stock_list(request, investor_id, portfolio_id):
    """

    :param request:
    :param investor_id:
    :param portfolio_id:
    :return:
    """

    if request.method == 'GET':
        return Response(stock_services.get_stocks_dicts(investor_id, portfolio_id))

    if request.method == 'POST':

        symbol = request.data['symbol']
        if jamstockex_api_service.is_stock_symbol_valid(symbol):
            stock_request_body = request.data
            stock_request_body['portfolio'] = portfolio_id
            serializer = StockSerializer(data=stock_request_body)

            return helper.save_serializer(serializer)
        return Response(CustomJsonResponse.return_portfolio_stock_not_found(), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@protected_resource()
def stocks_weights(request, investor_id, portfolio_id):
    """

    :param request:
    :param investor_id:
    :param portfolio_id:
    :return:
    """

    if request.method == 'GET':
        return Response(stock_services.get_stocks_weights_dicts(investor_id, portfolio_id), status=status.HTTP_200_OK)
