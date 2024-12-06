import os

from django.core.wsgi import get_wsgi_application

from config.env_reader import env

ENVIRONMENT = env.ENVIRONMENT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{ENVIRONMENT}")

application = get_wsgi_application()
