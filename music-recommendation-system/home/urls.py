from django.contrib import admin
from django.urls import path, include
from home import views
from pycode.music_rec import recommend

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path("recommend_music/", views.recommend_music, name="recommend_music"),
    path("music_list/",views.music_list,name="music_list")
]