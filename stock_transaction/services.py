import stock.services as stock_services
import transaction.services as transaction_services
from stock.serializers import StockSerializer


def create_stock_transaction(stock, transaction):
    try:

        # Create stock.
        stock_obj = stock_services.create_stock(stock)

        # Add stock id to request body.
        transaction['stock'] = stock_obj.data['id']
        return transaction_services.create_transaction(transaction)
    except Exception as e:
        print(e)
        raise e
