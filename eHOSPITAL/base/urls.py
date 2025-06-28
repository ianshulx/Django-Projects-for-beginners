from django.urls import path
from .views import HomePageView, CustomLoginView, CustomLogoutView, AboutPageView
from base import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path('', HomePageView.as_view(), name = 'home'),
    path('about/', AboutPageView.as_view(), name = 'about'),
    path('login/', CustomLoginView.as_view(), name = 'login'),
    path('logout/', CustomLogoutView.as_view(), name = 'logout')
   
]