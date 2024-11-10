from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('settings',views.settings,name="settings"),
    path('upload',views.upload,name="upload"),
    path('like_post',views.Like_post,name="Like_post"),
    path('comment',views.comment,name="comment"),
    path('profile/<str:username>',views.profile,name="profile"),
    path("follow/<str:username>",views.follow,name="follow"),
    path("post/<uuid:post_id>",views.post,name="post"),
    path('search',views.search,name="search")
]

urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)