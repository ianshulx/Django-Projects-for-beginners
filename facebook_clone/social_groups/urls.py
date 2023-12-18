from django.urls import path
from .views import group_list, group_detail


urlpatterns = [
    path('', group_list, name = 'group-list'),
    path('group-detail/<id>/', group_detail, name='group-detail')
]