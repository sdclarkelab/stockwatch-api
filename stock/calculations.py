from helper import round_to_2_sig


@round_to_2_sig
def calculate_market_value(market_price, shares):
    return market_price * shares


@round_to_2_sig
def calculate_stock_weight(market_value, total_market_value):
    return (market_value / total_market_value) * 100


@round_to_2_sig
def calculate_profit_value(market_value, total_value):
    return market_value - total_value


@round_to_2_sig
def calculate_profit_percentage(market_value, total_value):
    return ((market_value - total_value) / total_value) * 100 if total_value > 0 else 0
