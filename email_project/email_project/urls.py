from email_proj import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('api/',include('email_proj.urls'))
]
