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

    try:
        stock_payload = request.data['stock']
        transaction = request.data['transaction']

        if transaction['shares'] >= 1:
            stock = stock_services.create_stock(stock_payload)

            #  Add stock id to request body. ***DO NOT REMOVE***
            transaction_request = transaction
            transaction_request["stock"] = stock.data['id']

            transaction_request.update(transaction_services.get_transaction_calculation_response(transaction_request))

            serializer = TransactionSerializer(data=transaction_request)
            return helper.save_serializer(serializer)
        else:
            return Response({"detail": "Shares must be greater than 100."}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as create_stock_and_transaction_error:
        print(create_stock_and_transaction_error)
        return Response(CustomJsonResponse.return_server_error(),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
