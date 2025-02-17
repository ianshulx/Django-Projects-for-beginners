from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        if self.displayname:
            return self.displayname
        return self.user.username

    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return f"{settings.STATIC_URL}images/avatar.svg"
