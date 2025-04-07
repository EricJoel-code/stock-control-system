"""
ASGI config for stock_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
#from channels.routing import ProtocolTypeRouter, URLRouter
#from channels.auth import AuthMiddlewareStack
#import products.routing  # Crea este archivo en la app products

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_management.settings")

application = get_asgi_application