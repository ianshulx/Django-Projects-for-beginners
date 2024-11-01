# course_project/urls.py

from django.contrib import admin
from django.urls import path, include
from payment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.courses_list, name='courses_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/create-order/', views.create_order, name='create_order'),
    path('courses/<int:course_id>/payment-success/', views.payment_success, name='payment_success'),
    path('courses/<int:course_id>/payment-cancel/', views.payment_cancel, name='payment_cancel'),
]
