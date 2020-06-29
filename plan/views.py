from django.shortcuts import get_object_or_404
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response
import plan.calculations as plan_cal

import helper
import stock.services as stock_services
from .models import Plan
from .serializers import PlanSerializer


@api_view(['POST', 'PUT'])
@protected_resource()
def plan(request, investor_id, portfolio_id, symbol):
    """
    Create or delete a plan details to determine when to sell.
    """

    if request.method == 'POST':
        stock = stock_services.get_stock_serializer(investor_id, portfolio_id, symbol)
        request.data["stock"] = stock.id

        serializer = PlanSerializer(data=request.data)
        return helper.save_serializer(serializer)


@api_view(['PUT'])
@protected_resource()
def plan_detail(request, investor_id, portfolio_id, symbol):

    if request.method == 'PUT':
        plan = get_object_or_404(Plan, id=investor_id)
        serializer = PlanSerializer(plan, data=request.data, partial=True)
        return helper.update_serializer(serializer)
