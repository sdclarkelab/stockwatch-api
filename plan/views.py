from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
import plan.services as plan_services
import stock.services as stock_services
from utils.custom_json_resp import CustomJsonResponse
from .serializers import PlanSerializer


@api_view(['POST'])
@protected_resource()
def plan(request, investor_id, portfolio_id, symbol):
    """
    Create a stock plan.
    :param request:
    :param investor_id:
    :param portfolio_id:
    :param symbol:
    :return:
    """

    if request.method == 'POST':
        stock = stock_services.get_stock_serializer(investor_id, portfolio_id, symbol)
        request.data["stock"] = stock.id

        serializer = PlanSerializer(data=request.data)
        return helper.save_serializer(serializer)


@api_view(['GET', 'PUT', 'DELETE'])
@protected_resource()
def plan_detail(request, investor_id, portfolio_id, symbol, plan_id):
    plan = plan_services.get_plan(investor_id, portfolio_id, symbol, plan_id)

    if request.method == 'PUT':
        return helper.update_serializer(PlanSerializer(plan, data=request.data, partial=True))

    if request.method == 'GET':
        return Response(PlanSerializer(plan).data)

    if request.method == 'DELETE':
        plan.delete()
        return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)
