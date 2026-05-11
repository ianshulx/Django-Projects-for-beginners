from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment, BarberShop, Barber, Service
from datetime import datetime, timedelta


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['shop', 'barber', 'service', 'customer_name', 'customer_email', 
                 'customer_phone', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop'].queryset = BarberShop.objects.all()
        self.fields['shop'].widget.attrs.update({'class': 'form-control'})
        self.fields['barber'].widget.attrs.update({'class': 'form-control'})
        self.fields['service'].widget.attrs.update({'class': 'form-control'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        shop = cleaned_data.get('shop')
        barber = cleaned_data.get('barber')
        service = cleaned_data.get('service')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if not all([shop, barber, service, date, time]):
            return cleaned_data

        # Check if barber works at the selected shop
        if barber.shop != shop:
            raise ValidationError("Selected barber does not work at the selected shop.")

        # Check if service is available at the selected shop
        if service.shop != shop:
            raise ValidationError("Selected service is not available at the selected shop.")

        # Check if appointment time is within shop hours
        if time < shop.opening_time or time > shop.closing_time:
            raise ValidationError(
                f"Appointment time must be between {shop.opening_time} and {shop.closing_time}"
            )

        # Check if appointment would end after shop closing time
        appointment_end = datetime.combine(date, time) + timedelta(minutes=service.duration_minutes)
        appointment_end_time = appointment_end.time()
        
        if appointment_end_time > shop.closing_time:
            raise ValidationError(
                f"Service would end at {appointment_end_time}, which is after shop closing time"
            )

        # Check for existing appointments at the same time
        existing_appointments = Appointment.objects.filter(
            barber=barber,
            date=date,
            time=time,
            status__in=['scheduled', 'confirmed']
        ).exclude(pk=self.instance.pk)

        if existing_appointments.exists():
            raise ValidationError("This barber already has an appointment at this time.")

        # Check for overlapping appointments
        service_end_time = appointment_end_time
        overlapping_appointments = Appointment.objects.filter(
            barber=barber,
            date=date,
            status__in=['scheduled', 'confirmed']
        ).exclude(pk=self.instance.pk)

        for apt in overlapping_appointments:
            apt_end_time = (
                datetime.combine(date, apt.time) + 
                timedelta(minutes=apt.service.duration_minutes)
            ).time()
            
            # Check for time overlap
            if (time < apt_end_time and service_end_time > apt.time):
                raise ValidationError(
                    f"This barber has another appointment from {apt.time} to {apt_end_time}"
                )

        return cleaned_data


class ShopSelectionForm(forms.Form):
    shop = forms.ModelChoiceField(
        queryset=BarberShop.objects.all(),
        empty_label="Select a barber shop",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
