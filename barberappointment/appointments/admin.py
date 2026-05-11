from django.contrib import admin
from .models import BarberShop, Barber, Service, Appointment


@admin.register(BarberShop)
class BarberShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'opening_time', 'closing_time', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']


@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'phone', 'email', 'is_active', 'created_at']
    search_fields = ['name', 'phone', 'email', 'shop__name']
    list_filter = ['shop', 'is_active', 'created_at']
    list_editable = ['is_active']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'duration_minutes', 'price', 'is_active', 'created_at']
    search_fields = ['name', 'shop__name']
    list_filter = ['shop', 'is_active', 'duration_minutes', 'created_at']
    list_editable = ['is_active']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'shop', 'barber', 'service', 'date', 'time', 'status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'shop__name', 'barber__name']
    list_filter = ['shop', 'barber', 'service', 'status', 'date', 'created_at']
    list_editable = ['status']
    date_hierarchy = 'date'
    ordering = ['-date', '-time']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Appointment Details', {
            'fields': ('shop', 'barber', 'service', 'date', 'time', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
