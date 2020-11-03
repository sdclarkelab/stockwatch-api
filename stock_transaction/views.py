from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
import stock.services as stock_services
from services import jamstockex_api_service
from utils.custom_json_resp import CustomJsonResponse
from stock.serializers import StockSerializer


import transaction.services as transaction_services
from transaction.serializers import TransactionSerializer

import json


@api_view(['POST'])
@protected_resource()
def create_stock_and_transaction(request, investor_id, portfolio_id):

    stock = request.data['stock']
    symbol = stock['symbol']

    if jamstockex_api_service.is_stock_symbol_valid(symbol):
        stock['portfolio'] = portfolio_id
        serializer = StockSerializer(data=stock)

        helper.save_serializer(serializer)

        # body_unicode = request.body.decode('utf-8')
        # body_data = json.loads(body_unicode)
        transaction = request.data['transaction']

        if transaction['shares'] >= 1:
            # TODO: Remove stock service call and pass the stock id from post body
            stock = stock_services.get_stock_serializer(investor_id, portfolio_id, symbol)

            #  Add stock id to request body. ***DO NOT REMOVE***
            transaction_request = transaction
            transaction_request["stock"] = stock.id

            transaction_request.update(transaction_services.get_transaction_calculation_response(transaction_request))

            serializer = TransactionSerializer(data=transaction_request)
            return helper.save_serializer(serializer)
        else:
            return Response({"detail": "Shares must be greater than 100."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(CustomJsonResponse.return_portfolio_stock_not_found(), status=status.HTTP_400_BAD_REQUEST)
