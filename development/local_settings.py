import os
from stockwatch.settings import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e/s/~dso[r5_m9g7w2gkcqk%c4c-t^0f03sdls&6nkp^=e%31acj2m4+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

JAMSTOCKEX_API = 'http://localhost:5000/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stockwatch',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
