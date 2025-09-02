from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("", views.HomeView.as_view(), name="home"),
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
]
