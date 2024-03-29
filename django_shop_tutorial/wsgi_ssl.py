"""
WSGI config for django_shop_tutorial project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_shop_tutorial.settings")

application = get_wsgi_application()

# SSL
os.environ['HTTPS'] = "on"