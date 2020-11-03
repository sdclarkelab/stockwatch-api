import requests as req
import json
from django.conf import settings
from datetime import datetime


import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
except Exception as e:
    print(e)


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
        cached_data = None

        try:
            cached_data = r.get('stock')
        except Exception as error:
            print(error)
            pass

        response_last_updated_date = str(datetime.strptime(json.loads(cached_data)['lastUpdatedDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date())
        if cached_data and response_last_updated_date == today:
            response = json.loads(cached_data)

        else:
            jam_stock_res = req.get(f'{settings.JAMSTOCKEX_API}/stocks')
            try:
                r.set('stock', jam_stock_res.text)
            except Exception as error:
                print(error)
                pass
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
