release: python manage.py migrate && python manage.py loaddata portfolio_stock_status.json
web: gunicorn stockwatch.wsgi --log-file -