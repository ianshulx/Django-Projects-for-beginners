from uuid import uuid4
from django.conf import settings
from django.core.mail import send_mail
from django.utils.text import slugify
from .models import Hotel

def generate_random_token(): return str(uuid4())

def send_user_verification_mail(email, token):
    subject = 'Verify your email address'
    message = F"""Hi, please verify your email address by clicking on this link:
            127.0.0.1:8000/accounts/verify-account/{token}"""
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

def send_vendor_verification_mail(email, token):
    subject = 'Verify your email address'
    message = F"""Hi, please verify your email address by clicking on this link:
            127.0.0.1:8000/accounts/vendor/verify-account/{token}"""
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

def send_verification_otp(email, otp):
    subject = 'OTP for account login'
    message = f"Hi, please Use this OTP for logging in:{otp}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

def generate_slug(hotel_name):
    slug = slugify(hotel_name) + '-' + str(uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug = slug).exists(): return generate_slug(hotel_name)
    return slug
