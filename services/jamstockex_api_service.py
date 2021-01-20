import json
from datetime import datetime

import redis
import requests as req
from django.conf import settings

try:
    # TODO: Use environment variable for redis properties.
    r = redis.Redis(host='localhost', port=6379, db=0)
except Exception as e:
    print(e)


def is_stock_symbol_valid(symbol):
    is_valid = False

    stock_names = json.loads(r.get('stock_names'))

    symbols = [stock_name['symbol'] for stock_name in stock_names]

    if symbol in symbols:
        is_valid = True

    return is_valid


def get_market_price(symbol):
    response = req.get(settings.JAMSTOCKEX_API + symbol + '?projection=trade_info.market_price')
    return response.json()['trade_info']['market_price']


def _get_cached_jamstockex_stocks_and_last_updated_date():
    """
    Return stock dict if found in cache.
    :return: dict
    """
    try:
        stock_cache = r.get('stock')

        if not stock_cache:
            raise Exception("No cached stocks")

        # convert redis response to dictionary.
        response = json.loads(stock_cache)

        last_updated_date = response.get('lastUpdatedDate', dict())
        cached_last_updated_date = str(datetime.strptime(last_updated_date, '%Y-%m-%dT%H:%M:%S.%fZ').date())

        return response['result'], cached_last_updated_date

    except Exception as stock_cache_error:
        print(stock_cache_error)
        return dict(), str()


def get_jamstockex_stocks():
    """

    :return:
    """
    try:
        jam_stock_res = req.get(f'{settings.JAMSTOCKEX_API}/stocks')
        r.set('stock', jam_stock_res.text)

        stocks_objs = jam_stock_res.json()['result']

        return stocks_objs
    except Exception as error:
        print(error)
        return dict()


def get_stocks_infos():
    """

    :return:
    """
    try:

        stock_info, cached_last_updated_date = _get_cached_jamstockex_stocks_and_last_updated_date()

        if (not (stock_info or cached_last_updated_date)) or cached_last_updated_date == datetime.today().strftime(
                '%Y-%m-%d'):
            jse_stocks = get_jamstockex_stocks()

            if jse_stocks:
                stock_info = jse_stocks

        stock_names = [
            {
                'instrument_name': stocks_obj['instrument_name'],
                'symbol': stocks_obj['symbol']
            }
            for stocks_obj in stock_info
        ]

        sorted_stock_names = sorted(stock_names, key=lambda k: k['instrument_name'])
        r.set('stock_names', json.dumps(sorted_stock_names))

        return stock_info
    except Exception as e:
        print(e)
        print('Something went wrong')
        return {}


def get_stock_trade_info(symbol):
    try:
        response = req.get(f'{settings.JAMSTOCKEX_API}/stocks/{symbol}?projection=trade_info last_updated_date')
        return response.json().get('trade_info', {})
    except Exception as e:
        print(symbol)
        print(e)
