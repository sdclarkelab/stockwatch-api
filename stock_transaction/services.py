from django.http import JsonResponse

import plan.services as plan_service
import stock.services as stock_services
import transaction.services as transaction_services
from services import jamstockex_api_service


def create_stock_transaction(stock, transaction, plan):
    try:

        # Create stock.
        stock_obj = stock_services.create_stock(stock)

        # Add stock id to request body.
        transaction['stock'] = stock_obj.data['id']
        created_transaction = transaction_services.create_transaction(transaction)

        # Create stock plan
        stock_total = stock_services.get_stock_totals_by_id(stock_obj.data['id'])
        market_price = jamstockex_api_service.get_market_price(stock_obj.data['symbol'])
        created_plan = plan_service.create_stock_plan(plan, stock_total, market_price)

        return JsonResponse(
            {"plan": created_plan.data, "transaction": created_transaction.data, "stock": stock_obj.data})

    except Exception as e:
        print(e)
        raise e
