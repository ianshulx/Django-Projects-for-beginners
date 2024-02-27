from django.urls import path
from .views import ( index, postList, like_post, get_like_count, user_comment,
                     comment_count, create_post, userSharePost )
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('home/', index, name="index"),
    path('post-list/', postList, name='post-list'),
    path('like-post/<id>/', csrf_exempt(like_post), name='like-post'),
    path('get-like-count/<id>/', get_like_count, name="get-like-count"),
    path('user-comment/<id>/', csrf_exempt(user_comment), name='user-comment'),
    path('comment-count/<id>/', comment_count, name='comment-count1'),
    path('create-post/', (create_post), name='create-post'),
    path('user-share-post/<id>/', userSharePost, name='user-share-post')
]
