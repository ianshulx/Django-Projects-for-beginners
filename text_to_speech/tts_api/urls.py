from django.urls import path
from .views import TextToSpeechView

urlpatterns = [
    path('', TextToSpeechView.as_view(), name='text_to_speech'),
]