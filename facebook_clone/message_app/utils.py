from .models import PrivateChatRoom
from django.contrib.humanize.templatetags.humanize import naturalday
from datetime import datetime
from django.core.serializers.python import Serializer
from .constant import *

def find_or_create_private_chat(user1, user2):
    try:
        chat = PrivateChatRoom.objects.get(user1 = user1, user2 = user2)
    except PrivateChatRoom.DoesNotExist:
        try:
            chat = PrivateChatRoom.objects.get(user1 = user2, user2 = user1)
        except PrivateChatRoom.DoesNotExist:
            chat = PrivateChatRoom(user1 = user1, user2 = user2)
            chat.save()
    return chat


def calculate_timestamp(timestamp):
    #print(datetime.now())
    """
    1. Todat or yesterday:
        - EX: 'today at 10:56 AM'
        - EX: 'yesterday at 5:19 PM'
    2. other:
        - EX: 05/06/2020
        - EX: 12/12/2020
    """
    #today or yesterday
    if((naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday")):
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        ts = f"{naturalday(timestamp)} at {str_time}"
    #other day
    else:
        str_time = datetime.strftime(timestamp, "%m/%d/%Y")
        ts = f"{str_time}"
    return str(ts)


class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'msg_type': MSG_TYPE_MESSAGE})
        dump_object.update({'msg_id': str(obj.id)})
        dump_object.update({'user_id': str(obj.user.id)})
        dump_object.update({'username': str(obj.user.username)})
        #dump_object.update({'user': str(obj.room)})
        dump_object.update({'message': str(obj.content)})
        dump_object.update({'profile_image': str(obj.user.profile_image.url)})
        dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
        return dump_object