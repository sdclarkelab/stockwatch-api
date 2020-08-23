from helper import round_to_2_sig


@round_to_2_sig
def calculate_market_value(market_price, shares):
    if float(shares) > 0:
        return float(market_price) * float(shares)
    else:
        return 0


@round_to_2_sig
def calculate_stock_weight(market_value, total_market_value):
    return (float(market_value) / float(total_market_value)) * 100


@round_to_2_sig
def calculate_profit_value(market_value, total_value):
    return float(market_value) - float(total_value)


@round_to_2_sig
def calculate_profit_percentage(market_value, total_value):
    return ((float(market_value) - float(total_value)) / float(total_value)) * 100 if float(total_value) > 0 else 0
