# chat/routing.py
"""
from django.urls import re_path

from . import consumers

# TIPS: WebSocketConsumerは.as_asgi()で呼び出せる。
# TIPS: 一致したパターンは、コンシューマーの self.scope から参照できる。
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
"""

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', consumers.ChatConsumer.as_asgi()),
]

