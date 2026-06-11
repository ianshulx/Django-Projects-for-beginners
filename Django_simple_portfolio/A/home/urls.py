from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('english',views.EnglishView.as_view(),name='english'),
]