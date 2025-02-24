from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # The URL expects a numeric receiver_id
    re_path(r"ws/chat/(?P<receiver_id>\d+)/$", ChatConsumer.as_asgi()),
]
