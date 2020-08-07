from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
import stock.services as stock_services
import transaction.services as transaction_services
from utils.custom_json_resp import CustomJsonResponse
from .serializers import TransactionSerializer


@api_view(['GET', 'POST', 'DELETE'])
@protected_resource()
def add_transaction(request, investor_id, portfolio_id, symbol):
    """
    GET and POST to apply only transactions to existing stocks in a portfolio.
    :param portfolio_id:
    :param request:
    :param investor_id:
    :param symbol:
    :return:
    """

    if request.method == 'GET':
        transactions = transaction_services.get_transactions(investor_id, portfolio_id, symbol)
        return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        if request.data['shares'] >= 100:
            # TODO: Remove stock service call and pass the stock id from post body
            stock = stock_services.get_stock_serializer(investor_id, portfolio_id, symbol)

            #  Add stock id to request body. ***DO NOT REMOVE***
            transaction_request = request.data
            transaction_request["stock"] = stock.id

            transaction_request.update(transaction_services.get_transaction_calculation_response(transaction_request))

            serializer = TransactionSerializer(data=transaction_request)
            return helper.save_serializer(serializer)
        else:
            return Response({"detail": "Shares must be greater than 100."}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        transactions = transaction_services.delete_transactions(investor_id, portfolio_id, symbol)
        if transactions:
            return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@protected_resource()
def transaction_detail(request, investor_id, portfolio_id, symbol, transaction_id):
    transaction = transaction_services.get_transaction(investor_id, portfolio_id, symbol, transaction_id)

    if request.method == 'GET':
        return Response(TransactionSerializer(transaction).data)

    elif request.method == 'PUT':
        return helper.update_serializer(TransactionSerializer(transaction, data=request.data, partial=True))

    elif request.method == 'DELETE':
        transaction.delete()
        return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)
