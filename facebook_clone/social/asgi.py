import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from message_app.consumers import ChatConsumer
from social_groups.consumers import GroupConsumer
from notification_app.consumers import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("", NotificationConsumer.as_asgi()),
                path("group_chat/<room_id>/", GroupConsumer.as_asgi()),
                path("chat/<room_id>/", ChatConsumer.as_asgi()),
            ])
        )
    ),
})