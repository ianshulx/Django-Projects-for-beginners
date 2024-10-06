from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("dash/", views.DashView, name="dash"),
    path("login/", views.LoginView, name="login"),
    path("register/", views.RegisterView, name="register"),
    path("logout/", views.LogoutView, name="logout"),
    path("profile/", views.ProfileView, name="profile")
]
