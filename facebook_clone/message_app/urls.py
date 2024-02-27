from django.urls import path
from .views import private_chat_room_view, create_or_return_private_chat

urlpatterns = [
    path('', private_chat_room_view, name="private-chat-room"),
    path('create-or-return-private-chat/<user2_id>/', create_or_return_private_chat,
         name="create-or-return-private-chat")
]
