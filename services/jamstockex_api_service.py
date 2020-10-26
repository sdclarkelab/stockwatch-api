import requests as req
import json
from django.conf import settings
from datetime import datetime


import redis
r = redis.Redis(host='localhost', port=6379, db=0)


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
    try:

        # if response has previous date, pull from API otherwise pull from cache
        # jam_stock_res = req.get(f'{settings.JAMSTOCKEX_API}/stocks')
        # # r.set('stock', jam_stock_res.text)
        # response = jam_stock_res.json()

        # response_last_updated_date = datetime.strptime(response['lastUpdatedDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date()

        today = datetime.today().strftime('%Y-%m-%d')

        data = r.get('stock')
        response = None
        if data:
            response = json.loads(data)
        if not response:
            jam_stock_res = req.get(f'{settings.JAMSTOCKEX_API}/stocks')
            r.set('stock', jam_stock_res.text)
            response = jam_stock_res.json()

        else:
            response_last_updated_date = datetime.strptime(response['lastUpdatedDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date()

            if today != str(response_last_updated_date):
                jam_stock_res = req.get(f'{settings.JAMSTOCKEX_API}/stocks')
                r.set('stock', jam_stock_res.text)
                response = jam_stock_res.json()

        return response['result']
    except Exception as e:
        print(e)
        return {}


def get_stock_trade_info(symbol):
    try:
        response = req.get(f'{settings.JAMSTOCKEX_API}/stocks/{symbol}?projection=trade_info last_updated_date')
        return response.json().get('trade_info', {})
    except Exception as e:
        print(symbol)
        print(e)
