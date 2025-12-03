from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Hotel, HotelBooking, HotelUser
from datetime import datetime
from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60*2)
def index(r):
    hotels = Hotel.objects.all().select_related('hotel_owner').prefetch_related('amenities')
    if r.GET.get('search'): hotels = hotels.filter(name__icontains=r.GET.get('search'))
    if r.GET.get('sort'):
        sort_by = r.GET.get('sort')
        if sort_by == 'sort_low': hotels = hotels.order_by('hotel_offer_price')
        else: hotels = hotels.order_by('-hotel_offer_price')
    return render(r, "index.html", context={"hotels": hotels[:200]})

def detail_hotel(r, slug):
    if r.method == 'POST':
        hotel = Hotel.objects.get(hotel_slug=slug)
        days_count = (datetime.strptime(r.POST.get('check_out'), "%Y-%m-%d") - datetime.strptime(r.POST.get('check_in'), "%Y-%m-%d")).days
        if days_count <= 0:
            messages.error(r, 'Invalid Booking Date!')
            return redirect(detail_hotel)
        HotelBooking.objects.create(hotel=hotel, user=HotelUser.objects.get(id=r.user.id),
                                    booking_start_date=r.POST.get('check_in'), booking_end_date=r.POST.get('check_out'),
                                    booking_price=hotel.hotel_offer_price * days_count)
        messages.success(r, "Hotel booked successfully!")
        return redirect(index)
    return render(r, "details.html", context={"hotel": Hotel.objects.get(hotel_slug=slug)})