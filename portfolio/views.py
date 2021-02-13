from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import helper
import portfolio.services as portfolio_services
import stock.services as stock_services
from utils.custom_json_resp import CustomJsonResponse
from .serializers import PortfolioSerializer


@api_view(['POST', 'GET'])
@protected_resource()
def portfolio_list(request, investor_id):
    """
    Create portfolio.
    :param request:
    :param investor_id:
    :return:
    """

    if request.method == 'GET':
        #  Gets portfolios and return response
        portfolios = portfolio_services.get_portfolios(investor_id)
        return Response(PortfolioSerializer(portfolios, many=True).data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        # ------------------ Set Default Values -----------------#
        request.data['user'] = investor_id

        #  Set portfolio status to "Active" (1)
        request.data['status'] = 1
        # -------------------------------------------------------#

        serializer = PortfolioSerializer(data=request.data)
        return helper.save_serializer(serializer)


@api_view(['GET', 'PUT', 'DELETE'])
@protected_resource()
def portfolio_detail(request, investor_id, portfolio_id):
    """
    Retrieve, update or delete a portfolio.
    """

    #  Gets portfolio
    portfolio = portfolio_services.get_portfolio(investor_id, portfolio_id)

    if request.method == 'GET':
        portfolio_response = PortfolioSerializer(portfolio).data
        portfolio_response.update(stock_services.get_stocks_totals(investor_id, portfolio_id))
        return Response(portfolio_response, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        return helper.update_serializer(PortfolioSerializer(portfolio, data=request.data, partial=True))

    elif request.method == 'DELETE':
        portfolio.delete()
        return Response(CustomJsonResponse.return_successful_delete(), status=status.HTTP_200_OK)


@api_view(['GET'])
@protected_resource()
def portfolio_default(request, investor_id):
    """

    :param request:
    :param investor_id:
    :return:
    """
    if request.method == 'GET':
        portfolio_id = portfolio_services.get_default_portfolio_id(investor_id)
        response = {
            "portfolio_id": portfolio_id
        }
        return Response(response, status=status.HTTP_200_OK)
