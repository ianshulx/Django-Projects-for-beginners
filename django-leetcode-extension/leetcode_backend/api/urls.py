from django.urls import path 
from .views import solve_view

urlpatterns = [
        path('solve/', solve_view),
]