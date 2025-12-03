"""
URL configuration for oyo_clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
import accounts.views as views

urlpatterns = [
    path('user-login/', views.user_login_page, name='user-login'),
    path('vendor-login/', views.vendor_login_page, name='vendor-login'),
    path('logout/', views.logout_page, name='logout'),
    path('user-register/', views.user_register_page, name='user-register'),
    path('vendor-register/', views.vendor_register_page, name='vendor-register'),
    path('verify-account/<str:token>/', views.verify_user_email_token, name='user-verify'),
    path('vendor/verify-account/<str:token>/', views.verify_vendor_email_token, name='vendor-verify'),
    path('send-otp/<str:email>/', views.send_otp, name='send_otp'),
    path('<str:email>/verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/<str:email>/', views.resend_otp, name='resend_otp'),
    path('vendor/dashboard/', views.dashboard, name='dashboard'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
    path('<str:slug>/upload-images/', views.upload_hotel_images, name='upload_hotel_images'),
    path('delete-image/<int:image_id>/', views.delete_hotel_image, name='delete_hotel_image'),
    path('edit-hotel/<str:slug>/', views.edit_hotel_details, name='edit_hotel'),
    path('vendor/check-bookings/<str:slug>/', views.check_bookings, name='vendor_check_bookings'),
    path('user/check-bookings/', views.user_check_bookings, name='user_check_bookings'),
]
