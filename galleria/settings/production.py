from .base import *
import os

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')

try:
    from .local import *
except ImportError:
    pass
