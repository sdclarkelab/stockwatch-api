from django.shortcuts import get_object_or_404
from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
from stock.models import Stock
from utils.custom_json_resp import CustomJsonResponse
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['POST'])
@protected_resource()
def new_notification(request, investor_id, portfolio_id, stock_name):
    """
    Retrieve, update or delete a portfolio stock notification.
    """
    stock = get_object_or_404(Stock, portfolio__user__id=investor_id, portfolio=portfolio_id,
                              symbol=stock_name)

    if request.method == 'POST':
        request.data['stock'] = stock.id
        serializer = NotificationSerializer(data=request.data)
        return helper.save_serializer(serializer)


@api_view(['GET', 'PUT', 'DELETE'])
@protected_resource()
def notification_detail(request, investor_id, portfolio_id, stock_name, notification_id):
    """
    Retrieve, update or delete a portfolio stock notification.
    """

    notification = get_object_or_404(Notification, stock__portfolio__user__id=investor_id,
                                     stock__portfolio=portfolio_id, stock__symbol=stock_name,
                                     pk=notification_id)

    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        return helper.update_serializer(serializer)

    elif request.method == 'DELETE':

        notification.delete()
        return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)
