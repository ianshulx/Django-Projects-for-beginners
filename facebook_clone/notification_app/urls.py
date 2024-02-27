from django.urls import path
from .views import notification_index


urlpatterns = [
    path('', notification_index, name="notification-index")
]
