from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, time


class BarberShop(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    opening_time = models.TimeField(default=time(9, 0))
    closing_time = models.TimeField(default=time(18, 0))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Barber(models.Model):
    name = models.CharField(max_length=100)
    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, related_name='barbers')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    specialties = models.TextField(help_text="Comma-separated list of specialties")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.shop.name}"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(480)]
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, related_name='services')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.shop.name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, related_name='appointments')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, help_text="Additional notes for the appointment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']
        unique_together = ['barber', 'date', 'time']

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} on {self.date} at {self.time}"

    def clean(self):
        from django.core.exceptions import ValidationError
        from datetime import datetime, time
        
        # Check if the appointment time is within shop hours
        if self.time < self.shop.opening_time or self.time > self.shop.closing_time:
            raise ValidationError(
                f"Appointment time must be between {self.shop.opening_time} and {self.shop.closing_time}"
            )
        
        # Check if the appointment doesn't overlap with service duration
        appointment_end_time = (
            datetime.combine(datetime.today(), self.time) + 
            datetime.timedelta(minutes=self.service.duration_minutes)
        ).time()
        
        if appointment_end_time > self.shop.closing_time:
            raise ValidationError(
                f"Service would end at {appointment_end_time}, which is after shop closing time"
            )
