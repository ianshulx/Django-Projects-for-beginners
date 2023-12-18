from django.db import models
from django.conf import settings
from message_app.utils import find_or_create_private_chat
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from notification_app.models import Notification
from django.utils import timezone
# Create your models here.


class FriendsList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user", null=True)
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="friends")
    notifications = GenericRelation(Notification)

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

            content_type = ContentType.objects.get_for_model(self)
            self.notifications.create(
                target=self.user,
                from_user=account,
                redirect_url=f"{settings.BASE_URL}/friend/friend-detail/{account.pk}/",
                verb=f"You are now friends with {account.username}.",
                content_type=content_type,
            )
            self.save()

        for friend in self.friends.all():
            chat = find_or_create_private_chat(self.user, friend)
            chat.is_active = True
            chat.save()

    def remove_friend(self, account):
        """
        Remove a friend
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone
        """
        remover_friends_list = self  # person terminating the frienship

        # Remove friend from romover friends list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friends list
        friends_list = FriendsList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

        content_type = ContentType.objects.get_for_model(self)

        # Create notification for removee
        friends_list.notifications.create(
            target=removee,
            from_user=self.user,
            redirect_url=f"{settings.BASE_URL}/friend/friend-detail/{self.user.pk}/",
            verb=f"You are no longer friends with {self.user.username}.",
            content_type=content_type,
        )

        # Create notification for remover
        self.notifications.create(
            target=self.user,
            from_user=removee,
            redirect_url=f"{settings.BASE_URL}/friend/friend-detail/{removee.pk}/",
            verb=f"You are no longer friends with {removee.username}.",
            content_type=content_type,
        )

    def is_mutual_friend(self, friend):
        """
        Is this a friend
        """
        if friend in self.friends.all():
            return True
        return False

    @property
    def get_cname(self):
        return "FriendsList"


class FriendRequest(models.Model):
    """
    A friend request consist of two main parts:
        1. SENDER:
            - Person sending/initiating the friend request
        2. RECIEVER:
            - Person recieving the friend request
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reciever")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    notifications = GenericRelation(Notification)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept a friend request
        Update both SENSER and RECIEVER friend lists
        """
        reciever_friend_list = FriendsList.objects.get(user=self.reciever)
        if reciever_friend_list:
            content_type = ContentType.objects.get_for_model(self)

            # Update notification for RECEIVER
            receiver_notification = Notification.objects.get(target=self.reciever, content_type=content_type, object_id=self.id)
            receiver_notification.is_active = False
            receiver_notification.redirect_url = f"{settings.BASE_URL}/friend/friend-detail/{self.sender.pk}/"
            receiver_notification.verb = f"You accepted {self.sender.username}'s friend request."
            receiver_notification.timestamp = timezone.now()
            receiver_notification.save()
            reciever_friend_list.add_friend(self.sender)
            sender_friend_list = FriendsList.objects.get(user=self.sender)
            if sender_friend_list:
                # Create notification for SENDER
                self.notifications.create(
                    target=self.sender,
                    from_user=self.reciever,
                    redirect_url=f"{settings.BASE_URL}/friend/friend-detail/{self.reciever.pk}/",
                    verb=f"{self.reciever.username} accepted your friend request.",
                    content_type=content_type,
                )
                sender_friend_list.add_friend(self.reciever)
                self.is_active = False
                self.save()
            return receiver_notification

    def decline(self):
        """
        Decline a friend request
        It is "declined" by setting the 'is_active' field to false
        """
        self.is_active = False
        self.save()

        content_type = ContentType.objects.get_for_model(self)

        # Update notification for RECEIVER
        notification = Notification.objects.get(target=self.reciever, content_type=content_type, object_id=self.id)
        notification.is_active = False
        notification.redirect_url = f"{settings.BASE_URL}/friend/friend-detail/{self.sender.pk}/"
        notification.verb = f"You declined {self.sender}'s friend request."
        notification.from_user = self.sender
        notification.timestamp = timezone.now()
        notification.save()

        # Create notification for SENDER
        self.notifications.create(
            target=self.sender,
            verb=f"{self.reciever.username} declined your friend request.",
            from_user=self.reciever,
            redirect_url=f"{settings.BASE_URL}/friend/friend-detail/{self.reciever.pk}/",
            content_type=content_type,
        )

        return notification

    def cancel(self):
        """
        Cancel a friend request
        It is "cancelled" byy setting the 'is_active' field to False.
        This is only different with respect to "declining" through the notification that
        is generated.
        """

        self.is_active = False
        self.save()

        content_type = ContentType.objects.get_for_model(self)

        # Create notification for SENDER
        self.notifications.create(
            target=self.sender,
            verb=f"You cancelled the friend request to {self.reciever.username}.",
            from_user=self.reciever,
            redirect_url=f"{settings.BASE_URL}/friend/friend-detail/{self.reciever.pk}/",
            content_type=content_type,
        )

        notification = Notification.objects.get(target=self.reciever, content_type=content_type, object_id=self.id)
        notification.verb = f"{self.sender.username} cancelled the friend request sent to you."
        #notification.timestamp = timezone.now()
        notification.read = False
        notification.save()

    @property
    def get_cname(self):
        return "FriendRequest"
    

@receiver(post_save, sender=FriendRequest)
def create_notification(sender, instance, created, **kwargs):
	if created:
		instance.notifications.create(
			target=instance.reciever,
			from_user=instance.sender,
			redirect_url=f"{settings.BASE_URL}/friend/friend-detail/{instance.sender.pk}/",
			verb=f"{instance.sender.username} sent you a friend request.",
			content_type=instance,
		)


'''from chat.utils import find_or_create_private_chat
from friend.models import FriendsList
friend_lists = FriendsList.objects.all()
for f in friend_lists:
    for friend in f.friends.all():
        chat = find_or_create_private_chat(f.user, friend)
        chat.is_active = True
        chat.save()'''
