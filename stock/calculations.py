def calculate_market_value(market_price, shares):
    if float(shares) > 0:
        return float(market_price) * float(shares)
    else:
        return 0


def calculate_stock_weight(market_value, total_market_value):
    return (float(market_value) / float(total_market_value)) * 100


def calculate_profit_value(market_value, total_value):
    return float(market_value) - float(total_value)


def calculate_profit_percentage(market_value, total_value):
    return ((float(market_value) - float(total_value)) / float(total_value)) * 100 if float(total_value) > 0 else 0
