from django.urls import path, re_path
from . import consumers

ws_urlpatterns = [
    path('ws/quiz-stream', consumers.QuizConsumer.as_asgi()),
    re_path(r"ws/notify/", consumers.NotificationConsumer.as_asgi()),
]
