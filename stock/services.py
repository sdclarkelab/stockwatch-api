from django.shortcuts import get_object_or_404

import stock.calculations as stock_cal
import transaction.services as trans_services
from services import jamstockex_api_service
import stock.services as stock_services
from .models import Stock, StockCalculatedDetail
from .serializers import StockSerializer, StockCalculatedDetailSerializer
from django.db import connection


#  -------------------------------------
#               Serializers
#  -------------------------------------
def get_stock_serializer(investor_id, portfolio_id, symbol):
    stock = get_object_or_404(Stock, portfolio__user__id=investor_id, portfolio=portfolio_id, symbol=symbol)
    return stock


def get_stocks_serializers(investor_id, portfolio_id):
    stocks = Stock.objects.filter(portfolio__user__id=investor_id, portfolio=portfolio_id)
    return stocks


def get_stocks_dicts(investor_id, portfolio_id):
    stocks = StockSerializer(get_stocks_serializers(investor_id, portfolio_id), many=True).data
    return stocks


def get_stock_transaction_detail():
    # with connection.cursor() as cursor:
    #     cursor.execute('select ss.symbol, sum(tt.shares) as total_shares, sum(tt.net_amount) as total_net_amount, '
    #                    'CAST((sum(tt.net_amount)/nullif(sum(tt.shares),0)) AS DECIMAL(10,2)) as avg_amount from '
    #                    'stock_stock ss LEFT JOIN transaction_transaction tt ON ss.id = tt.stock_id GROUP BY ss.symbol;')
    #     row = cursor.fetchall()
    #
    # return row
    try:
        stockDetail = StockCalculatedDetail.objects.raw(
            'select ss.id as id, ss.symbol, sum(tt.shares) as total_shares, sum(tt.net_amount) as total_net_amount, '
            'CAST((sum(tt.net_amount)/nullif(sum(tt.shares),0)) AS DECIMAL(10,2)) as avg_amount, '
            '(sum(tt.shares) * CAST((sum(tt.net_amount)/nullif(sum(tt.shares),0)) AS DECIMAL(10,2))) as total_value '
            'from stock_stock ss  '
            'LEFT JOIN transaction_transaction tt ON ss.id = tt.stock_id GROUP BY ss.symbol, ss.id;')
        seq = StockCalculatedDetailSerializer(stockDetail, many=True).data

        return seq
    except Exception as e:
        print(e)


def get_stock_calculated_detail(investor_id, portfolio_id, symbol, transactions_info):
    # transactions_info = trans_services.get_stock_transaction_detail(investor_id, portfolio_id, symbol)

    market_position = jamstockex_api_service.get_stock_trade_info(symbol)

    if transactions_info and market_position:
        market_position['market_value'] = stock_cal.calculate_market_value(market_position['market_price'],
                                                                           transactions_info['total_shares'])

        if market_position['market_value'] > 0:
            stock_performance = {
                'profit_loss_value': stock_cal.calculate_profit_value(market_position['market_value'],
                                                                      transactions_info['total_value']),
                'profit_loss_percentage': stock_cal.calculate_profit_percentage(market_position['market_value'],
                                                                                transactions_info['total_value'])
            }

            stock_weights = stock_services.get_stocks_weights_dicts(investor_id, portfolio_id)
            stock_weight = 0
            for weight in stock_weights:
                if symbol == weight['stock']:
                    stock_weight = weight['weight_percentage']
                    break

            return {
                'symbol': symbol,
                'market_position': market_position,
                'performance': stock_performance,
                'transaction_info': transactions_info,
                'stock_weight': stock_weight
            }
        else:
            return None
    else:
        return {
            'symbol': symbol,
            'market_position': {},
            'performance': {},
            'transaction_info': {}
        }


def get_stock_detail_dict(investor_id, portfolio_id, symbol):
    stock_serializer = StockSerializer(get_stock_serializer(investor_id, portfolio_id, symbol)).data
    stock_calculated_dict = get_stock_calculated_detail(investor_id, portfolio_id, symbol)

    stock_serializer.update(stock_calculated_dict)

    return stock_serializer


def get_stocks_weights_dicts(investor_id, portfolio_id):
    # Calculate stocks market values
    market_values = get_total_market_values_dicts(investor_id, portfolio_id)

    stock_weights = []
    for stock in market_values['stocks']:
        stock_weight = {'stock': '', 'weight_percentage': 0}
        stock_weight['stock'] = stock['symbol']
        stock_weight['weight_percentage'] = stock_cal.calculate_stock_weight(stock['market_price'],
                                                                             market_values['total'])

        stock_weights.append(stock_weight)

    return stock_weights


def get_total_market_values_dicts(investor_id, portfolio_id):
    total_market_values_dicts = {'total': 0,
                                 'stocks': []}

    #  Get market price
    market_positions = jamstockex_api_service.get_stocks_infos()

    # Get Transaction info
    transactions_infos = trans_services.get_all_stocks_transaction_details(investor_id, portfolio_id)

    for transactions_info in transactions_infos:
        # market_price = next(item['trade_info']['market_price'] for item in market_positions if
        #                     item["symbol"] == transactions_info['symbol'])
        market_price = 0
        for item in market_positions:
            if item["symbol"] == transactions_info['symbol'] and "trade_info" in item:
                market_price = item['trade_info']['market_price']

        stock_market_dict = {'symbol': '', 'market_price': 0}

        stock_market_dict['symbol'] = transactions_info['symbol']
        stock_market_dict['market_price'] = stock_cal.calculate_market_value(market_price,
                                                                             transactions_info['total_shares'])
        total_market_values_dicts['stocks'].append(stock_market_dict)

        total_market_values_dicts['total'] += stock_cal.calculate_market_value(market_price,
                                                                               transactions_info['total_shares'])

    return total_market_values_dicts


def update_stock_total_market_value(stocks, investor_id, portfolio_id):
    total_market_value = 0
    for stock in stocks:
        # TODO: Refactor code
        stock.update(get_stock_calculated_detail(investor_id, portfolio_id, stock['symbol']))
        total_market_value += stock['market_position']['market_value']

    return total_market_value


def get_stocks_totals(investor_id, portfolio_id):
    stocks = get_stocks_dicts(investor_id, portfolio_id)
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
