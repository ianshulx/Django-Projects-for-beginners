from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("login/", views.LoginView, name="login"),
]
