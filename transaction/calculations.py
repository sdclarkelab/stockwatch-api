from helper import round_to_2_sig


@round_to_2_sig
def calculate_gross_amount(transaction):
    return float(transaction['price']) * int(transaction['shares'])


@round_to_2_sig
def calculate_net_amount(transaction):
    if transaction['action'] == 'buy':
        return calculate_gross_amount(transaction) + float(transaction['fees'])
    return calculate_gross_amount(transaction) - float(transaction['fees'])


@round_to_2_sig
def calculate_net_price(transaction):
    return calculate_net_amount(transaction) / float(transaction['shares'])


@round_to_2_sig
def calculate_total_net_price(transactions):
    total = 0
    for transaction in transactions:
        total += calculate_net_price(transaction)

    return total


@round_to_2_sig
def calculate_average_price(transactions):
    return calculate_total_net_price(transactions) / len(transactions)


def calculate_total_units(transactions):
    total = 0
    for transaction in transactions:
        total += transaction['shares']

    return total


@round_to_2_sig
def calculate_current_value(transactions):
    return calculate_average_price(transactions) * calculate_total_units(transactions)


@round_to_2_sig
def calculate_total_net_amount(transactions):
    total = 0
    for transaction in transactions:
        total += float(transaction['net_amount'])

    return total
