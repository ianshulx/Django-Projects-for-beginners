# downloader/urls.py
from django.urls import path
from .views import stream_video_from_url

app_name = 'downloader'

urlpatterns = [
    path('', stream_video_from_url, name='home'),
]
