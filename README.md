# StockWatchJa API
This is the server for the StockWatchJa application. It pulls stock trade data from **[StockWatchJA: JamStockEx API](https://github.com/sdclarkelab/jamstockex-api)** at this [URL](http://jamstockexapi.stockwatchja.com/stocks).

## API Documentation
Click [here](https://documenter.getpostman.com/view/6678518/S1TU3eAz) to view the API documentation.

## Requirements
Tool | Version  | Source |
--- | --- | --- |
Python |3.7.4| [Python 3.7.4 Release](https://www.python.org/downloads/release/python-374/)|
Heroku|-|[Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)|
Windows OS| 10 | - | 
Docker| 19.03.4| [Docker Desktop](https://www.docker.com/products/docker-desktop)|

### Setup Dev

#### Create Django dev setting file
Export settings module: 
- On Windows: `set DJANGO_SETTINGS_MODULE=development.local_settings`
- On Linux: `export DJANGO_SETTINGS_MODULE=development.local_settings`


#### Create and initialize Docker database 
``` shell script
# Create Postgres database Docker container and create schema
> python development/dev_setup.py

# Create admin user
> python manage.py createsuperuser
```

#### Test Super User Credentials

```shell script
> python manage.py runserver 5555
```

Login to [admin page](http://127.0.0.1:5555/api/v1/stockwatch_admin/) with super user credentials to confirm it works.
(use "***[custom_admin_page](http://docker_ip_add/api/v1/stockwatch_admin/)***" if the docker-machine ip is not using the default IP address)


#### Register Application

Go to [application registration](http://127.0.0.1:5555/api/v1/stockwatch_admin/o/applications/) and complete the form.
(use "***[custom application registration](http://docker_ip_add/api/v1/stockwatch_admin/o/applications/)***" if the docker-machine ip is not using the default IP address)
> Name: StockwatchAPI
>
> Client type: Confidential
>
> Authorization grant type: Resource owner password-based
