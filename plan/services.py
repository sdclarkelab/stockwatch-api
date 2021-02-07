from django.shortcuts import get_object_or_404

import helper
from .models import Plan, PlanStatus
from .serializers import PlanSerializer, PlanStatusSerializer


def get_plan(investor_id, portfolio_id, symbol, plan_id):
    plan = get_object_or_404(Plan, stock__portfolio__user__id=investor_id,
                             stock__portfolio=portfolio_id, stock__symbol=symbol, pk=plan_id)

    return plan


def get_plan_by_id(plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    return plan


def get_pan_statuses():
    try:
        plan_statues = PlanStatus.objects.all()
        return PlanStatusSerializer(plan_statues, many=True).data
    except Exception as e:
        print(e)
        raise e


def create_plan_in_db(plan):
    try:
        serializer = PlanSerializer(data=plan)
        return helper.save_serializer(serializer)
    except Exception as e:
        print(e)
        raise e


def create_stock_plan(plan, stock_total):
    try:

        plan['stock'] = stock_total['id']
        plan['target_sell_price'] = calculate_target_sell_price(plan['target_percentage'], stock_total['avg_net_price'])

        status = ''
        if plan['target_sell_price'] > stock_total['avg_net_price']:
            status = 'hold'
        else:
            status = 'sell'

        plan_statues = get_pan_statuses()
        plan_status = next(item for item in plan_statues if item["status_name"] == status)

        plan['status'] = plan_status['id']
        del plan['target_percentage']
        created_plan = create_plan_in_db(plan)
        return created_plan
    except Exception as e:
        print(e)
        raise e


def calculate_target_sell_price(target_percentage, avg_net_price):
    try:
        target_sell_price = 0

        target_sell_price = float(avg_net_price) * (
                float(target_percentage) / 100) + float(avg_net_price)

        target_sell_price = float("{:.2f}".format(target_sell_price))

        return target_sell_price
    except Exception as e:
        print(e)
        raise e


def update_stock_plan(plan_id, stock_total):
    """

    :param plan_id:
    :param stock_total:
    :return:
    """
    try:

        plan = get_plan_by_id(plan_id)
        updated_plan = PlanSerializer(plan).data
        updated_plan['target_sell_price'] = calculate_target_sell_price(10, stock_total['avg_net_price'])

        if updated_plan['target_sell_price'] > stock_total['avg_net_price']:
            status = 'hold'
        else:
            status = 'sell'

        plan_statues = get_pan_statuses()
        plan_status = next(item for item in plan_statues if item["status_name"] == status)

        return helper.update_serializer(PlanSerializer(plan, data=updated_plan, partial=True))

    except Exception as e:
        print(e)
        raise e
