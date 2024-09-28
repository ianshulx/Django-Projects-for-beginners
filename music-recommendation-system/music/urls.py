"""
URL configuration for music project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from login.views import loginaction
from signup.views import signaction
from song_list.views import musiclistaction
from sign_out.views import signout
from contactus.views import contactaction
from aboutus.views import aboutusaction
from musichome.views import musichomeaction

urlpatterns = [
    path('',include('home.urls')),
    path("admin/", admin.site.urls),
    path('login/',loginaction),
    path('signup/',signaction),
    path('song_list/', musiclistaction),
    path('sign_out/',signout),
    path('contactus/',contactaction),
    path('aboutus/',aboutusaction),
    path('musichome/',musichomeaction),
]

