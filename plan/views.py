from django.shortcuts import get_object_or_404
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
import stock.services as stock_services
from .models import Plan
from .serializers import PlanSerializer


@api_view(['GET'])
@protected_resource()
def plans(request, investor_id, portfolio_id, symbol):
    if request.method == 'GET':
        stock_dicts = stock_services.get_stocks_dicts(investor_id, portfolio_id)
        response = []
        for stocks in stock_dicts:
            response.append(stock_services.get_stock_calculated_detail(investor_id, portfolio_id, stocks['symbol']))

        return Response(response)


@api_view(['GET', 'POST', 'PUT'])
@protected_resource()
def plan_detail(request, investor_id, portfolio_id, symbol):
    """
    Retrieve, update or delete a plan details to determine when to sell.
    """
    #  Gets stock

    if request.method == 'GET':
        stock = stock_services.get_stock_serializer(investor_id, portfolio_id, symbol)
        # plan = Plan.objects.get(stock=stock.id)

        # serializer = PlanSerializer(plan).data
        stock_detail = stock_services.get_stock_calculated_detail(investor_id, portfolio_id, symbol)
        # should_sell = plan_cal.calculate_should_sell(stock_detail['transaction_info']['average_price'],
        #                                              plan.target_sell_price)
        #
        # val = 'SELL' if should_sell else 'HOLD'
        #
        # serializer.update({'action': val})
        return Response(stock_detail)

    elif request.method == 'POST':
        stock = stock_services.get_stock_serializer(investor_id, portfolio_id, symbol)
        request.data["stock"] = stock.id

        serializer = PlanSerializer(data=request.data)
        return helper.save_serializer(serializer)

    elif request.method == 'PUT':
        plan = get_object_or_404(Plan, id=investor_id)
        serializer = PlanSerializer(plan, data=request.data, partial=True)
        return helper.update_serializer(serializer)
