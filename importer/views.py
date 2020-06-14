import csv

from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response
import helper
import transaction.services as transaction_services
from stock.serializers import StockSerializer
from transaction.serializers import TransactionSerializer


@api_view(['POST'])
@protected_resource()
def jmmb_importer(request, investor_id, portfolio_id):
    """
    Retrieve, update or delete a stock.
    """
    if request.method == 'POST':
        stock_response = None

        with open(request.data['test'].name, mode='rb') as csv_file:
            transactions = csv.DictReader(csv_file)
            next(transactions)
            symbols = set([transaction["SYMBOL"] for transaction in transactions])

        # # Read CSV
        # with open('jmmb_equity_orders.csv', mode='r') as csv_file:
        #     transactions = csv.DictReader(csv_file)
        #     next(transactions)
        #
        #     # Extract Symbols and bulk insert into DB using stock
        #     symbols = set([transaction["SYMBOL"] for transaction in transactions])
        #     stock_body = [{"symbol": symbol, "portfolio": portfolio_id} for symbol in symbols]
        #     serializer = StockSerializer(data=stock_body, many=True)
        #     stock_response = helper.save_serializer(serializer)
        #
        #     if (stock_response):
        #
        #         stocks = {stock["symbol"]: stock["id"] for stock in stock_response.data}
        #         csv_file.seek(0)
        #         transactions = csv.DictReader(csv_file)
        #         next(transactions)
        #
        #         new_transactions = [{
        #             "stock": stocks[transaction["SYMBOL"]],
        #             "action": str(transaction["TRANSACTION TYPE"]).lower(),
        #             "price": transaction["TRADE PRICE"],
        #             "shares": int(transaction["ORDER QUANTITY"]),
        #             "fees": transaction["CHARGES"]
        #         } for transaction in transactions]
        #
        #         for new_transaction in new_transactions:
        #             new_transaction.update(transaction_services.get_transaction_calculation_response(new_transaction))
        #
        #         serializer = TransactionSerializer(data=new_transactions, many=True)
        #         return helper.save_serializer(serializer)
