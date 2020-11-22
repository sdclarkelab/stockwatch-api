import os
import time


def create_db():
    print('Creating services ...')
    os.system('cd _docker_configs && docker-compose -p "stockwatch" up -d')


def create_tables():
    print('Create DB tables ...')
    os.system('python manage.py migrate && python manage.py loaddata portfolio_stock_status.json')


if __name__ == "__main__":
    create_db()
    print('Initializing DB ...')
    time.sleep(3)
    create_tables()

