from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/text/', consumers.MyConsumer.as_asgi()),
]
