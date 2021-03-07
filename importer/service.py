import pandas as pd

import plan.services as plan_service
import stock.services as stock_services
import stock_transaction.services as stock_transaction_services
import transaction.services as transaction_services


def save_jmmb_uploaded_file(investor_id, portfolio_id, jmmb_file):
    data = pd.read_csv(jmmb_file)

    # Get transaction action
    trans_action = {
        'SELL': 1,
        'BUY': 2
    }

    for index, row in data.iterrows():
        if row['SYMBOL'] != 'CWJ' and row['SYMBOL'] != 'FIRSTROCKJMD':
            stock_obj = stock_services.get_stock_by_symbol(investor_id, portfolio_id, row['SYMBOL'], False)

            if row['TRANSACTION TYPE'] == 'BUY' and not stock_obj:
                stock = {
                    "portfolio": portfolio_id,
                    "symbol": row['SYMBOL'],
                    "status": 1
                }

                transaction = {
                    "action": trans_action[row['TRANSACTION TYPE']],
                    "price": row['TRADE PRICE'],
                    "shares": row['ORDER QUANTITY'],
                    "fees": row['CHARGES']
                }

                plan = {
                    "target_percentage": 20
                }

                print(f"BUY => Order date => {row['ORDER DATE']} symbol {row['SYMBOL']} price {row['TRADE PRICE']}")
                stock_transaction_services.create_stock_transaction(stock, transaction, plan)
            if stock_obj:
                stock_totals = stock_services.get_stock_totals()
                stock_total = next(item for item in stock_totals if item["symbol"] == row['SYMBOL'])

                plan_id = plan_service.get_plan_id_by_stock_id(stock_total['id'])

                transaction = {
                    "action": trans_action[row['TRANSACTION TYPE']],
                    "price": row['TRADE PRICE'],
                    "shares": row['ORDER QUANTITY'],
                    "fees": row['CHARGES'],
                    "stock": stock_obj['id'],
                    "total_shares": stock_total['total_shares'],
                    "plan_id": plan_id
                }
                print(f"SELL => Order date => {row['ORDER DATE']} symbol {row['SYMBOL']} price {row['TRADE PRICE']}")
                transaction_services.create_transaction_and_update_stock(transaction, investor_id, portfolio_id,
                                                                         stock_total['id'])
