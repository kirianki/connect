import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import listings.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connect_platform.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            listings.routing.websocket_urlpatterns
        )
    ),
})
