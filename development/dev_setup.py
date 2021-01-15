import os
import time


def create_db():
    print('Creating services ...')
    os.system('cd development/_docker_configs && docker-compose -p "stockwatch" up -d')


def create_tables():
    print('Create DB tables ...')
    os.system('python manage.py migrate && python manage.py loaddata portfolio_stock_status.json plan_plan_status.json fixture_transaction_action')


if __name__ == "__main__":
    create_db()
    print('Initializing DB ...')
    time.sleep(3)
    create_tables()

