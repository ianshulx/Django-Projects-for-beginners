from itertools import chain
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import json
from message_app.utils import find_or_create_private_chat
from .models import PrivateChatRoom
from account.models import Accounts
# Create your views here.

DEBUG = True


def private_chat_room_view(request, *args, **kwargs):
    context = {}
    user = request.user
    room_id = request.POST.get("room_id")
    if not user.is_authenticated:
        return HttpResponse("This user is not authenticated")

    if room_id:
        try:
            room = PrivateChatRoom.objects.get(pk=room_id)
            print(room)
            context['room'] = room
        except PrivateChatRoom.DoesNotExist:
            pass

    room1 = PrivateChatRoom.objects.filter(user1=user, is_active=True)
    room2 = PrivateChatRoom.objects.filter(user2=user, is_active=True)
    print(room2)
    rooms = list(chain(room1, room2))
    
    m_and_f = []

    for room in rooms:
        if room.user1 == user:
            friend = room.user2
        else:
            friend = room.user1
        m_and_f.append({
            "message": "",
            "friend": friend
        })
    context["m_and_f"] = m_and_f
    context['debug'] = DEBUG
    context['debug_mode'] = settings.DEBUG

    return render(request, "message_app/message.html", context)


def create_or_return_private_chat(request, *args, **kwargs):
    user1 = request.user
    payload = {}
    if user1.is_authenticated:
        if request.method == "POST":
            user2_id = kwargs.get("user2_id")
            print(user2_id)
            try:
                user2 = Accounts.objects.get(pk=user2_id)
                chat = find_or_create_private_chat(user1, user2)
                print(chat.id)
                payload['response'] = "Successfully got the chat"
                payload['chatroom_id'] = chat.id
            except Accounts.DoesNotExist:
                payload['response'] = "Unable to start a chat with that user."
    else:
        payload['response'] = "You can't start a chat if you are not authenticated."
    return HttpResponse(json.dumps(payload), content_type="application/json")
