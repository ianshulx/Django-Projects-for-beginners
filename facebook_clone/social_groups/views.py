from django.shortcuts import render
from django.conf import settings
from .models import GroupChatRoom

# Create your views here.
DEBUG = False

"""
Group Chat List
"""

def group_list(request):
    user = request.user
    if user.is_authenticated:
        group_list = GroupChatRoom.objects.all()
        context = {
            'group_list': group_list
        }
    return render(request, 'group_list.html', context)


"""
Group Chat
"""
def group_detail(request, id):
    room_id = GroupChatRoom.objects.get(id = id)
    user = request.user
    context = {
        'room_id': room_id.pk,
        'room_detail': room_id,
        'debug_mode': settings.DEBUG,
        'debug': DEBUG,
        'user': user
    }
    return render(request, 'group_detail.html', context)
