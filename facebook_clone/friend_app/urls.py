from django.urls import path
from .views import (friend_index, send_friend_request, accept_friend_request, decline_friend_request, cancel_friend_request, remove_friend, friend_detail)

urlpatterns = [
    path('', friend_index, name='friend-index'),
    path('send-friend-request/<user_id>/',
         send_friend_request, name='send-friend-request'),
    path('accept-friend-request/<pending_friend_id>/',
         accept_friend_request, name="accept-friend-request"),
    path('decline-friend-request/<pending_friend_id>/',
         decline_friend_request, name="decline-friend-request"),
    path('cancel_friend_request/<receiver_user_id>/',
         cancel_friend_request, name="cancel_friend_request"),
    path('remove_friend/<receiver_user_id>/',
         remove_friend, name="remove_friend"),
     path('friend-detail/<user_id>/', friend_detail, name="friend-detail")
]
