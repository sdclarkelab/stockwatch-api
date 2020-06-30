from django.shortcuts import get_object_or_404

from .models import Plan


def get_plan(investor_id, portfolio_id, symbol, plan_id):
    plan = get_object_or_404(Plan, stock__portfolio__user__id=investor_id,
                             stock__portfolio=portfolio_id, stock__symbol=symbol, pk=plan_id)

    return plan
