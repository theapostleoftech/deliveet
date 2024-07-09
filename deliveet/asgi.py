"""
ASGI config for deliveet project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deliveet.settings')

django_application = get_asgi_application()

from . import urls  # noqa isort:skip

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(urls.websocket_urlpatterns)
    }
)
