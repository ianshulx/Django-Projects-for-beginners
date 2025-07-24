from django.urls import path
from . import views


urlpatterns = [
    path("", views.Home, name="home"),
    path("article/<int:pk>", views.ArticleDetails, name="article_details"),
    path("add_article", views.AddArticle, name="add_article"),
    path("edit_article/<int:pk>", views.EditArticle, name="edit_article"),
    path("delete_article/<int:pk>", views.DeleteArticle, name="delete_article"),
    path("signup", views.SignUp.as_view(), name="signup"),
    path("change_password", views.ChangePassword, name="password_change"),
]
