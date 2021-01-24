from django.shortcuts import get_object_or_404

from .models import Portfolio


def get_portfolios(investor_id):
    #  TODO: Apply filter and search for GET method
    #  TODO: return stock count...can be a calculated value and not be stored in DB
    portfolios = Portfolio.objects.fetch(user__id=investor_id)

    return portfolios


def get_portfolio(investor_id, portfolio_id):
    portfolio = get_object_or_404(Portfolio, user__id=investor_id, pk=portfolio_id)

    return portfolio


def get_default_portfolio_id(investor_id):
    """

    :param investor_id:
    :return:
    """
    portfolio = get_object_or_404(Portfolio, user__id=investor_id, is_default=True)
    return portfolio.id
