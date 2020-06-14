from django.db.models import Sum, Avg, F, FloatField, ExpressionWrapper
from django.shortcuts import get_object_or_404

import transaction.calculations as trans_cal
from .models import Transaction
from .serializers import TransactionInfoSerializers, TransactionInfoSerializer


def get_all_transactions(investor_id, portfolio_id):
    transactions = Transaction.objects.filter(stock__portfolio__user__id=investor_id,
                                              stock__portfolio__id=portfolio_id)
    return transactions


def get_transactions(investor_id, portfolio_id, symbol):
    transactions = Transaction.objects.filter(stock__portfolio__user__id=investor_id,
                                              stock__portfolio__id=portfolio_id, stock__symbol=symbol)
    return transactions


def get_transaction(investor_id, portfolio_id, symbol, transaction_id):
    transaction = get_object_or_404(Transaction, stock__portfolio__user__id=investor_id,
                                    stock__portfolio=portfolio_id, stock__symbol=symbol, pk=transaction_id)

    return transaction


def delete_transactions(investor_id, portfolio_id, symbol):
    transactions = Transaction.objects.filter(stock__portfolio__user__id=investor_id,
                                              stock__portfolio__id=portfolio_id, stock__symbol=symbol).delete()

    return transactions


def get_transaction_calculation_response(transaction):
    transaction_response = {
        'gross_amount': trans_cal.calculate_gross_amount(transaction),
        'net_amount': trans_cal.calculate_net_amount(transaction),
        'net_price': trans_cal.calculate_net_price(transaction)
    }

    if transaction['action'] == 'sell':
        transaction['shares'] = int(transaction['shares']) * -1

    return transaction_response


def get_stock_transaction_detail(investor_id, portfolio_id, symbol):
    transactions_raw = Transaction.objects.filter(stock__portfolio__user__id=investor_id,
                                                  stock__portfolio__id=portfolio_id, stock__symbol=symbol) \
        .values('stock').annotate(total_shares=Sum('shares'), average_price=Avg('net_price')) \
        .annotate(total_value=ExpressionWrapper(F('total_shares') * F('average_price'), output_field=FloatField()))

    transactions = TransactionInfoSerializer(transactions_raw, many=True).data[0]
    return transactions


def get_all_stocks_transaction_details(investor_id, portfolio_id):
    transactions_raw = Transaction.objects.filter(stock__portfolio__user__id=investor_id,
                                                  stock__portfolio__id=portfolio_id) \
        .values('stock').annotate(total_shares=Sum('shares'), average_price=Avg('net_price')) \
        .annotate(total_value=ExpressionWrapper(F('total_shares') * F('average_price'), output_field=FloatField())) \
        .annotate(symbol=F('stock__symbol'))

    transactions = TransactionInfoSerializers(transactions_raw, many=True).data

    return transactions

