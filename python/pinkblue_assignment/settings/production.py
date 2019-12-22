from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = []

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

try:
    from .local import *
except:
    pass
