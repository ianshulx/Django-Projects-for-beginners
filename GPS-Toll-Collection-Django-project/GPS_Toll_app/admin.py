from django.contrib import admin
from .models import Profile, Vehicle_details , Trip


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','auth_token', 'isverified', 'created_at']
    
@admin.register(Vehicle_details)
class VehicleDetailsAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'vehicle_type', 'vehicle_model', 'vehicle_company', 'vehicle_color', 'created_at', 'updated_at')
    
    search_fields = ('vehicle_number', 'vehicle_model', 'vehicle_company')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'vehicle_type', 'starting_point', 'ending_point', 'date_entered', 'total_km', 'destination_reached_time', 'total_amount','uuid_field','charge_per_km')
    search_fields = ('vehicle_number__vehicle_number', 'starting_point', 'ending_point','charge_per_km')

