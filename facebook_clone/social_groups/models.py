from django.db import models
from django.conf import settings

# Create your models here.


class GroupChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, help_text="Users who are connected to the chat")

    def __str__(self):
        return self.title

    def connect_user(self, user):
        """
        return true if user is added to the users list4
        """
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        """
        return true if user is removed from the users list
        """
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        """
        Returns the channel group name that sockets should subscribe to and get sent messages
        as they are generated
        """
        return f"{self.title}-{self.id}"


class PublicRoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs

class PublicRoomChatMessage(models.Model):
    """
    Chat message created by a user inside a Public chat room (foreign key)
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique = False, blank = False)

    objects = PublicRoomChatMessageManager()

    def __str__(self):
        return self.content