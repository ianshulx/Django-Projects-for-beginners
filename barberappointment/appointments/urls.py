from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('api/barbers-and-services/', views.get_barbers_and_services, name='get_barbers_and_services'),
    path('api/check-availability/', views.check_availability, name='check_availability'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]
