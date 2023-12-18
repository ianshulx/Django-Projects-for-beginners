from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from friend_app.models import FriendRequest, FriendsList
from notification_app.models import Notification
# Create your views here.


def notification_index(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        friend_request_ct = ContentType.objects.get_for_model(FriendRequest)
        friend_list_ct = ContentType.objects.get_for_model(FriendsList)
        notifications = Notification.objects.filter(target=user, content_type__in=[friend_request_ct, friend_list_ct]).order_by('-timestamp')
        #print(notifications)
        context['notifications'] = notifications
    return render(request, 'notification_app/notification.html', context)
