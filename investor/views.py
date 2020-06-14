from django.shortcuts import get_object_or_404
from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
from utils.custom_json_resp import CustomJsonResponse
from .models import Investor
from .serializers import InvestorSerializer

from django.http import JsonResponse


@api_view(['POST'])
def new_investor(request):
    """
    Create an investor.
    :param request:
    :return:
    """
    if request.method == 'POST':

        serializer = InvestorSerializer(data=request.data)
        return helper.save_serializer(serializer)


@api_view(['GET'])
@protected_resource()
def get_investor_id(request):

    if request.method == 'GET':
        response = {'user_id': request.user.id}
        return JsonResponse(response)


@api_view(['GET', 'PUT', 'DELETE'])
@protected_resource()
def investor_profile(request, investor_id):
    """
    Create, Edit and View an investor profile.
    :param request:
    :param investor_id: Investor ID
    :return:
    """

    #  Gets investor object
    investor = get_object_or_404(Investor, id=investor_id)

    if request.method == 'GET':
        serializer = InvestorSerializer(investor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = InvestorSerializer(investor, data=request.data, partial=True)
        return helper.update_serializer(serializer)

    elif request.method == 'DELETE':
        investor.delete()
        return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)
