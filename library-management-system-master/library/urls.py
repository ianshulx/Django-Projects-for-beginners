from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^adminpage/$', views.create_user, name='create_user'),
    url(r'^create-student/(?P<username>[\w.@+-]+)/(?P<admin>[\w.@+-]+)$', views.create_student, name='create_student'),
    url(r'^create-staff/(?P<username>[\w.@+-]+)/(?P<admin>[\w.@+-]+)$', views.create_staff, name='create_staff'),    
    url(r'^ajax/change_request_issue/$', views.change_request_issue, name='change_request_issue'),
    url(r'^student-dashboard/$', views.student_dashboard, name='student_dashboard'),
    url(r'^ajax/change_issue_status/$', views.change_issue_status, name='change_issue_status'),
    url(r'^staff-issue/$', views.staff_issue, name='staff_dashboard'),
    url(r'^staff-addbook/$', views.staff_addbook, name='staff_addbook'),
    
]