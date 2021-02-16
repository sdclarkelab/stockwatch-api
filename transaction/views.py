from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import transaction.services as transaction_services
from utils.custom_json_resp import CustomJsonResponse
from .serializers import TransactionSerializer


@api_view(['GET', 'POST', 'DELETE'])
@protected_resource()
def add_transaction(request, investor_id, portfolio_id, stock_id):
    """
    GET and POST to apply only transactions to existing stocks in a portfolio.
    :param portfolio_id:
    :param request:
    :param investor_id:
    :param stock_id:
    :return:
    """

    if request.method == 'GET':
        transactions = transaction_services.get_transactions(investor_id, portfolio_id, stock_id)
        return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        return transaction_services.create_transaction_and_update_stock(request.data, investor_id, portfolio_id,
                                                                        stock_id)

    elif request.method == 'DELETE':
        transactions = transaction_services.delete_transactions(investor_id, portfolio_id, stock_id)
        if transactions:
            return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@protected_resource()
def transaction_detail(request, investor_id, portfolio_id, stock_id, transaction_id):
    """

    :param request:
    :param investor_id:
    :param portfolio_id:
    :param stock_id:
    :param transaction_id:
    :return:
    """
    if request.method == 'GET':
        transaction = transaction_services.get_transaction(investor_id, portfolio_id, stock_id, transaction_id)
        return Response(TransactionSerializer(transaction).data)

    elif request.method == 'PUT':
        return transaction_services.update_transaction(investor_id, portfolio_id, stock_id, transaction_id,
                                                       request.data)

    elif request.method == 'DELETE':
        transaction_services.delete_transaction(investor_id, portfolio_id, stock_id, transaction_id)
        return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)
