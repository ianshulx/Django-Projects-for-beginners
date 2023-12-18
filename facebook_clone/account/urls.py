from django.urls import path
from .views import register_view, login_view, logout_view, forgot_password, resetPass

urlpatterns = [
    path('register/', register_view, name = 'register'),
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-pass/<uidb64>/<token>', resetPass, name='reset-user-pass')
]