from . import views
from django.urls import path

urlpatterns = [
    path('',views.user_request,name="user_request"),
    path('/submit',views.submit_form,name="submit_form"),
]
