from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "carts",
]


REDIS_URL = os.getenv("REDIS_URL")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

ROOT_URLCONF = "config.urls"