# from .models import *
# from django.contrib.auth.models import User


# from django.dispatch import receiver
# from django.db.models.signals import post_save

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):  
#     if created and not instance.is_superuser: 
#        Profile_google.objects.create(
#             user=instance,
#             firstname=instance.first_name,
#             lastname=instance.last_name,
#             email=instance.email
#         )

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile_google.save()

