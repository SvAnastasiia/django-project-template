import os

from django.core.asgi import get_asgi_application

from config.env_reader import env

ENVIRONMENT = env.ENVIRONMENT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{ENVIRONMENT}")

application = get_asgi_application()
