from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",   # temp
]


DATABASES = {
 "default": {
   "ENGINE": "django.db.backends.postgresql",
   "NAME": os.getenv("POSTGRES_DB"),
   "USER": os.getenv("POSTGRES_USER"),
   "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
   "HOST": os.getenv("POSTGRES_HOST"),
   "PORT": os.getenv("POSTGRES_DB_PORT", 5432),
   "OPTIONS": {
       "sslmode": "require",
   },
 }
}


# SECURE_HSTS_SECONDS setting

SECURE_HSTS_SECONDS = 31536000  # 1 year

SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# for production: to redirect all connections to HTTPS
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
