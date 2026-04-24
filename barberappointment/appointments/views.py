from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from .models import BarberShop, Barber, Service, Appointment
from .forms import AppointmentForm, ShopSelectionForm


def home(request):
    """Home page showing all barber shops"""
    shops = BarberShop.objects.all()
    return render(request, 'appointments/home.html', {'shops': shops})


def shop_detail(request, shop_id):
    """Detail view for a specific barber shop"""
    shop = get_object_or_404(BarberShop, id=shop_id)
    barbers = shop.barbers.filter(is_active=True)
    services = shop.services.filter(is_active=True)
    
    return render(request, 'appointments/shop_detail.html', {
        'shop': shop,
        'barbers': barbers,
        'services': services,
    })


def book_appointment(request):
    """View for booking a new appointment"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment booked successfully for {appointment.customer_name}!')
            return redirect('appointment_confirmation', appointment_id=appointment.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_date = timezone.now().date()
        form = AppointmentForm(initial={'date': initial_date})
    
    return render(request, 'appointments/book_appointment.html', {'form': form})


def appointment_confirmation(request, appointment_id):
    """Confirmation page after successful booking"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointments/confirmation.html', {'appointment': appointment})


def get_barbers_and_services(request):
    """AJAX endpoint to get barbers and services for a selected shop"""
    shop_id = request.GET.get('shop_id')
    if not shop_id:
        return JsonResponse({'error': 'Shop ID is required'}, status=400)
    
    try:
        shop = BarberShop.objects.get(id=shop_id)
        barbers = [{'id': b.id, 'name': b.name} for b in shop.barbers.filter(is_active=True)]
        services = [{'id': s.id, 'name': s.name, 'duration': s.duration_minutes, 
                    'price': str(s.price)} for s in shop.services.filter(is_active=True)]
        
        return JsonResponse({
            'barbers': barbers,
            'services': services,
            'shop_hours': {
                'opening': str(shop.opening_time),
                'closing': str(shop.closing_time)
            }
        })
    except BarberShop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)


def check_availability(request):
    """Check available time slots for a barber on a specific date"""
    barber_id = request.GET.get('barber_id')
    date_str = request.GET.get('date')
    service_id = request.GET.get('service_id')
    
    if not all([barber_id, date_str, service_id]):
        return JsonResponse({'error': 'Missing required parameters'}, status=400)
    
    try:
        barber = Barber.objects.get(id=barber_id)
        service = Service.objects.get(id=service_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Get existing appointments for the barber on that date
        existing_appointments = Appointment.objects.filter(
            barber=barber,
            date=date,
            status__in=['scheduled', 'confirmed']
        ).order_by('time')
        
        # Generate available time slots
        available_slots = []
        current_time = datetime.combine(date, barber.shop.opening_time)
        end_time = datetime.combine(date, barber.shop.closing_time)
        
        # Convert existing appointments to time ranges
        occupied_ranges = []
        for apt in existing_appointments:
            apt_start = datetime.combine(date, apt.time)
            apt_end = apt_start + timedelta(minutes=apt.service.duration_minutes)
            occupied_ranges.append((apt_start, apt_end))
        
        # Find available slots
        while current_time + timedelta(minutes=service.duration_minutes) <= end_time:
            slot_end = current_time + timedelta(minutes=service.duration_minutes)
            
            # Check if this slot conflicts with any existing appointment
            is_available = True
            for occupied_start, occupied_end in occupied_ranges:
                if (current_time < occupied_end and slot_end > occupied_start):
                    is_available = False
                    break
            
            if is_available:
                available_slots.append({
                    'time': current_time.time().strftime('%H:%M'),
                    'available': True
                })
            
            # Move to next 30-minute slot
            current_time += timedelta(minutes=30)
        
        return JsonResponse({'available_slots': available_slots})
        
    except (Barber.DoesNotExist, Service.DoesNotExist, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


def my_appointments(request):
    """View appointments for a customer (by email or phone)"""
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        if not email and not phone:
            messages.error(request, 'Please provide either email or phone number.')
            return render(request, 'appointments/my_appointments.html')
        
        appointments = Appointment.objects.filter(
            Q(customer_email=email) | Q(customer_phone=phone)
        ).order_by('-date', '-time')
        
        return render(request, 'appointments/my_appointments.html', {
            'appointments': appointments,
            'search_email': email,
            'search_phone': phone
        })
    
    return render(request, 'appointments/my_appointments.html')


def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        # Simple verification - in production, you'd want better authentication
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        if appointment.customer_email == email or appointment.customer_phone == phone:
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
        else:
            messages.error(request, 'Email or phone does not match our records.')
        
        return redirect('my_appointments')
    
    return render(request, 'appointments/cancel_appointment.html', {'appointment': appointment})
