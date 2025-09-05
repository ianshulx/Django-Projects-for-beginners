from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.loginview, name="login"),
    path('signup/', views.signupview, name="signup"),
    path('logout/', views.logoutview, name="logout")
]