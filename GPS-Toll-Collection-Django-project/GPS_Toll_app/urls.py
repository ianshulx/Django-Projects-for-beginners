from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authrization/register/', views.register_attempt, name='register_attempt'),
    path('authrization/login/', views.login_attempt, name='login_attempt'),
    path('pricing/<str:username>', views.pricing, name='pricing'),
    path('enquiry/<str:username>', views.enquiry, name='enquiry'),
    path('authrization/verify/<auth_token>', views.verify, name='verify'),
    path('authrization/logout/', views.logout_attempt, name='logout'),
    path('authrization/error/', views.error_page, name='error_page'),
    path('authrization/forget_password/', views.forget_password, name='forget_password'),
    path('authrization/change_password/ <auth_token>/', views.change_password, name='change_password'),
    path('authrization/vehicle_details/<str:username>', views.vehicle_details, name='vehicle_details'),
    path('authrization/Add_vehicle/<str:username>', views.Add_vehicle, name='Add_vehicle'),
    path('authrization/delete_vehicle/<str:username>/<str:vehicle_number>/', views.delete_vehicle, name='delete_vehicle'),
    
    
    path('authrization/pricing/download/<str:username>/<str:filename>/', views.download_pdf, name='download_pdf'),
    
    path('authrization/pricing/pay_now/<str:username>/<str:filename>/', views.pay_now, name='pay_now'),
    
    path('authrization/pricing/paybill/<str:username>/<str:filename>/', views.paybill, name='paybill'),
    
    
    
    path('Trip/', views.Trips_fun, name='Trip'),
    path('Trip/simulation/invoice/', views.invoice, name='invoice'),
    path('Trip/simulation/generate_pdf/<str:username>/<str:uuid_field_value>', views.generate_pdf, name='generate_pdf'),
    path('Trip/simulation/<str:filename>', views.simulation, name='simulation'),
    path('Trip/get-coordinates/<str:filename>/', views.get_coordinates, name='get_coordinates'),
    path('Trip/store-coordinate/', views.store_coordinate, name='store_coordinate'),
    
]

    
    # path('Trip/display-map/<str:filename>/', views.display_map, name='display_map'),
    
    
    # path('Trip/get-coordinates/<path:filename>/', views.get_coordinates, name='get_coordinates'),
    
