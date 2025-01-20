from django.urls import path, re_path
from chat.consumers import chatConsumer


websocket_urlpatterns = [
    # re_path(r"ws/chat/?$",chatConsumer.as_asgi())
    
    re_path(r"ws/chat/(?P<username>\d+)/$", chatConsumer.as_asgi())
]