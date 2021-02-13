from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import stock_transaction.services as stock_transaction_services
from utils.custom_json_resp import CustomJsonResponse


@api_view(['POST'])
@protected_resource()
def create_stock_and_transaction(request, investor_id, portfolio_id):
    """
    Adds a stock to the database and it's first transaction.
    :param request:
    :param investor_id:
    :param portfolio_id:
    :return:
    """
    try:
        stock_payload = request.data['stock']
        transaction_payload = request.data['transaction']
        plan_payload = request.data['plan']

        return stock_transaction_services.create_stock_transaction(stock_payload, transaction_payload, plan_payload)

    except Exception as create_stock_and_transaction_error:
        print(create_stock_and_transaction_error)
        return Response(CustomJsonResponse.return_server_error(),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
