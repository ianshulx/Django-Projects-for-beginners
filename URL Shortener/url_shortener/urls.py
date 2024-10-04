from django.contrib import admin
from django.urls import path
from .views import Urlgenerate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Urlgenerate.as_view(), name="home")
]
