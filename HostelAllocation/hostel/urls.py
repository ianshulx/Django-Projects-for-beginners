from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('view_application/', views.view_application, name='view_application'),
    path('rector/dashboard/', views.rector_dashboard, name='rector_dashboard'),
    path('allocate/', views.allocate_seats, name='allocate'),
    path('view_allocation/', views.view_allocation, name='view_allocation'),
    path('logout/', views.logout_view, name='logout'),
]
