# yourapp/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Profile
from django.utils import timezone

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(
                user=user,
                auth_token='google',
                isverified=True,
                created_at=timezone.now()
            )
        return user
