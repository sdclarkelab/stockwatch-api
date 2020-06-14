def calculate_total_units(transaction_type, transaction_unit_amount, total_units):
    if transaction_type == "buy":
        total_units = transaction_unit_amount + total_units

    else:
        if total_units > transaction_unit_amount:
            total_units = total_units - transaction_unit_amount

        else:
            total_units = -1

    return total_units
