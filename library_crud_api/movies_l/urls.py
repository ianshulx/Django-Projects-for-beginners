from django.urls import path
from . import views

app_name = 'movies'
# Create your routes here.

urlpatterns = [
    path('', views.movies, name='movies_list'),
    path('detail/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('create/', views.movie_create, name='movie_create'),
    path('update/<int:pk>/', views.movie_update, name='movie_update'),
    path('delete/<int:pk>/', views.movie_delete, name='movie_delete'),
]
