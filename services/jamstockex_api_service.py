import requests as req
from django.conf import settings


def is_stock_symbol_valid(symbol):
    is_valid = False

    #  Get response from AWS lambda function
    response = req.get(f'{settings.JAMSTOCKEX_API}/stocks/{symbol}?projection=symbol')

    if response.status_code == 200 and response.json():
        is_valid = True

    return is_valid


def get_market_price(symbol):
    response = req.get(settings.JAMSTOCK_API + symbol + '?projection=trade_info.market_price')
    return response.json()['trade_info']['market_price']


def get_stocks_infos():
    response = req.get(f'{settings.JAMSTOCKEX_API}/stocks')
    return response.json()


def get_stock_trade_info(symbol):
    try:
        response = req.get(f'{settings.JAMSTOCKEX_API}/stocks/{symbol}?projection=trade_info last_updated_date')
        return response.json().get('trade_info', {})
    except Exception as e:
        print(symbol)
        print(e)
