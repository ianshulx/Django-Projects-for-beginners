from django.urls import path
from . import views

app_name = 'books'

# Create your routes here.

urlpatterns = [
    path('', views.books, name='books_list'),
    path('detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('create/', views.book_create, name='book_create'),
    path('update/<int:pk>/', views.book_update, name='book_update'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
]
