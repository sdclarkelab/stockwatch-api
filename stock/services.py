import json
from datetime import datetime

import redis
from django.shortcuts import get_object_or_404

import helper
import stock.calculations as stock_cal
from services import jamstockex_api_service
from .models import Stock, StockCalculatedDetail
from .serializers import StockSerializer, StockCalculatedDetailSerializer

try:
    # TODO: Use environment variable for redis properties.
    r = redis.Redis(host='localhost', port=6379, db=0)
except Exception as e:
    print(e)


#  -------------------------------------
#               Serializers
#  -------------------------------------
def get_stock_serializer(investor_id, portfolio_id, symbol):
    stock = get_object_or_404(Stock, portfolio__user__id=investor_id, portfolio=portfolio_id, symbol=symbol)
    return stock


def get_stocks_serializers(investor_id, portfolio_id):
    stocks = Stock.objects.filter(portfolio__user__id=investor_id, portfolio=portfolio_id)
    return stocks


def get_stocks(investor_id, portfolio_id):
    stocks = StockSerializer(get_stocks_serializers(investor_id, portfolio_id), many=True).data
    return stocks


def get_stock_totals():
    try:

        stock_totals = StockCalculatedDetail.objects.raw(
            'select '
            'st.id, '
            'st.symbol, '
            'st.total_shares, '
            'snt.avg_net_price, '
            'snt.total_net_amount, '
            '(snt.avg_net_price * st.total_shares) as current_value '
            'from '
            '( '
            'select '
            'ss.id as id, ss.symbol, sum(tt.net_amount) as total_net_amount, cast((sum(tt.net_amount)/ '
            'nullif(sum(tt.shares), 0)) as DECIMAL(10, 2)) as avg_net_price '
            'from '
            'stock_stock ss '
            'left join transaction_transaction tt on '
            'ss.id = tt.stock_id '
            'where '
            'tt."action" in (\'buy\')  and ss.is_archived in (\'0\') '
            'group by '
            'ss.symbol, ss.id '
            'having '
            'ss.status_id = 3 ) snt '
            'left join ( '
            'select '
            'ss.id as id, ss.symbol, sum(tt.shares) as total_shares '
            'from '
            'stock_stock ss '
            'left join transaction_transaction tt on '
            'ss.id = tt.stock_id '
            'group by '
            'ss.symbol, ss.id ) st on '
            '(st.id = snt.id) '
            'order by '
            'st.symbol'
        )

        return StockCalculatedDetailSerializer(stock_totals, many=True).data
    except Exception as e:
        print(e)


def create_stock_performance_response(stock_totals, stock_index_data_list):
    try:

        stock_details = []
        total_market_value = 0
        total_current_value = 0

        for stock_total in stock_totals:

            symbol = stock_total['symbol']

            stock_detail = {
                'id': stock_total['id'],
                'symbol': stock_total['symbol'],
                'market_position': {},
                'performance': {},
                'transaction_info': {},
                'stock_weight': {}
            }

            # Get Market object
            stock_index_data = next((item.get('trade_info', {}) for item in stock_index_data_list if
                                     item.get('symbol', {}) == symbol and item.get('currency', {}) == 'JMD'), None)

            if stock_index_data and "market_price" in stock_index_data and stock_total['total_shares'] > 0:
                market_value = stock_cal.calculate_market_value(stock_index_data['market_price'],
                                                                stock_total['total_shares'])

                total_market_value += market_value
                total_current_value += stock_total['current_value']

                # Update stock detail response
                stock_detail['transaction_info'] = stock_total
                stock_detail['market_position'] = stock_index_data
                stock_detail['market_position']['market_value'] = market_value
                stock_detail['performance'] = {
                    'profit_loss_value': stock_cal.calculate_profit_value(market_value,
                                                                          stock_total['current_value']),
                    'profit_loss_percentage': stock_cal.calculate_profit_percentage(market_value,
                                                                                    stock_total[
                                                                                        'current_value'])
                }
                stock_details.append(stock_detail)

        for stock_detail in stock_details:
            stock_detail['stock_weight']['owned'] = stock_cal.calculate_stock_weight(
                stock_detail['transaction_info']['current_value'], total_current_value)
            stock_detail['stock_weight']['market'] = stock_cal.calculate_stock_weight(
                stock_detail['market_position']['market_value'], total_market_value)

        return stock_details
    except Exception as e:
        print(e)


def get_total_market_value(symbol, market_price, total_shares, total_market_values_dicts):
    stock_market_dict = {'symbol': symbol, 'market_price': stock_cal.calculate_market_value(market_price, total_shares)}

    total_market_values_dicts['stocks'].append(stock_market_dict)

    total_market_values_dicts['total'] += stock_cal.calculate_market_value(market_price, total_shares)

    return total_market_values_dicts


def update_stock_total_market_value(stocks, investor_id, portfolio_id):
    total_market_value = 0
    for stock in stocks:
        # TODO: Refactor code
        # stock.update(get_stock_calculated_detail(investor_id, portfolio_id, stock['symbol']))
        total_market_value += stock['market_position']['market_value']

    return total_market_value


def get_stocks_totals(investor_id, portfolio_id):
    stocks = get_stocks(investor_id, portfolio_id)
    total_market_value = 0
    total_current_value = 0
    for stock in stocks:
        total_market_value += stock['market_value']
        total_current_value += stock['total_value']

    stock_totals = {
        'total_current_value': total_current_value,
        'total_market_value': total_market_value
    }

    return stock_totals


def get_stock_names_from_cache():
    """
    Returns list of stock instrument names and symbol. Eg [{'instrument_name': 'Best Stock', 'symbol': 'BestSk'}]
    :return:
    """
    try:
        return json.loads(r.get('stock_names'))
    except Exception as get_stock_names_from_cache_error:
        print(get_stock_names_from_cache_error)
        return []


def create_stock(stock):
    try:
        if jamstockex_api_service.is_stock_symbol_valid(stock['symbol']):
            stock["created_date"] = datetime.today()
            stock["is_archived"] = False
            serializer = StockSerializer(data=stock)
            return helper.save_serializer(serializer)
    except Exception as create_stock_error:
        print(create_stock_error)
