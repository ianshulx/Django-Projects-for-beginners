from django.shortcuts import render, redirect
import accounts.models as models
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import accounts.utils as utils
from django.contrib.auth import authenticate, login, logout
from random import randint
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_login_page(r):
    if r.method == 'POST':
        email = r.POST.get('email')
        password = r.POST.get('password')
        user_obj = models.HotelUser.objects.filter(email=email)
        if not user_obj.exists():
            messages.error(r, 'No Account Found!')
            return redirect(user_login_page)
        if not user_obj[0].is_verified:
            messages.error(r, 'Account Not Verified!')
            return redirect(user_login_page)
        hotel_user = authenticate(username=user_obj[0].username,password=password)
        if hotel_user:
            login(r, hotel_user)
            messages.success(r, 'Login Successful!')
            return redirect('/')
        messages.error(r, 'Login Failed!')
        return redirect(user_login_page)
    return render(r, "user/login.html")

def user_register_page(r):
    if r.method == 'POST':
        first_name = r.POST.get('first_name')
        last_name = r.POST.get('last_name')
        email = r.POST.get('email')
        phone_number = r.POST.get('phone_number')
        pass1 = r.POST.get('password1')
        pass2 = r.POST.get('password2')
        if models.HotelUser.objects.filter(Q(email=email) | Q(phone_number=phone_number)).exists():
            messages.error(r, "Account exists with email or phone number.")
            return redirect(user_login_page)
        if pass1 == pass2:
            hotel_user = models.HotelUser.objects.create(first_name=first_name, last_name=last_name,
                                                 email=email, phone_number=phone_number,
                                                 email_token=utils.generate_random_token(), username=phone_number)
            hotel_user.set_password(pass1)
            hotel_user.save()
            utils.send_user_verification_mail(email, hotel_user.email_token)
            messages.success(r, "Account created successfully.")
            return redirect(user_login_page)
    return render(r, "user/register.html")

def verify_user_email_token(r, token):
    try:
        hotel_user = models.HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(r, 'Account Verified Successfully!')
        return redirect(user_login_page)
    except models.HotelUser.DoesNotExist:
        return HttpResponse('<h2>Invalid token.</h2>')

def verify_vendor_email_token(r, token):
    try:
        hotel_user = models.HotelVendor.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(r, 'Account Verified Successfully!')
        return redirect(user_login_page)
    except models.HotelUser.DoesNotExist:
        return HttpResponse('<h2>Invalid token.</h2>')

def logout_page(r):
    logout(r)
    messages.success(r, 'Logout Successful!')
    return redirect('/')

def send_otp(r, email):
    user_obj = models.HotelUser.objects.filter(email=email).exists()
    if not user_obj:
        messages.error(r, 'User Does not exist')
        redirect(user_register_page)
    otp = randint(100000, 999999)
    utils.send_verification_otp(email, otp)
    r.session['otp'] = otp
    r.session.set_expiry(180)
    return redirect(f'/accounts/{email}/verify-otp')

def verify_otp(r, email):
    if r.method == 'POST':
        otp = r.POST.get('otp')
        user_obj = models.HotelUser.objects.get(email=email)
        if 'otp' not in r.session:
            messages.error(r, 'OTP Expired!')
            return redirect(f'/resend-otp/{email}')
        if int(otp) == r.session.get('otp'):
            messages.success(r, 'OTP Verified! Login Successful!')
            login(r, user_obj)
            r.session.pop('otp', None)
            return redirect('/')
        messages.warning(r, 'Wrong OTP!')
        return redirect(f'/accounts/{email}/verify-otp')
    return render(r, 'user/verify_otp.html')

def resend_otp(r, email):
    if not models.HotelUser.objects.filter(email=email).exists():
        messages.error(r, 'Invalid User')
        return redirect(user_register_page)
    otp = randint(100000, 999999)
    utils.send_verification_otp(email, otp)
    r.session['otp'] = otp
    r.session.set_expiry(180)
    messages.success(r, 'OTP Resent to your email!')
    return redirect(f'/accounts/{email}/verify-otp')

def vendor_login_page(r):
    if r.method == 'POST':
        email = r.POST.get('email')
        user_obj = models.HotelVendor.objects.filter(email=email)
        password = r.POST.get('password')
        if not user_obj.exists():
            messages.error(r, 'Vendor not registered!')
            return redirect(vendor_register_page)
        if not user_obj[0].is_verified:
            messages.warning(r, 'Vendor not verified!')
            return redirect(vendor_login_page)
        hotel_vendor = authenticate(username=user_obj[0].username ,password=password)
        if hotel_vendor:
            login(r, hotel_vendor)
            messages.success(r, 'Vendor Login Successful!')
            return redirect(dashboard)
    return render(r, 'vendor/login.html')

def vendor_register_page(r):
    if r.method == 'POST':
        phone_number = r.POST.get('phone_number')
        email = r.POST.get('email')
        if models.HotelVendor.objects.filter(Q(phone_number=phone_number) | Q(email=email)).exists():
            messages.error(r, 'Vendor already registered!')
            return redirect(vendor_login_page)
        pass1 = r.POST.get('password1')
        pass2 = r.POST.get('password2')
        if pass1 != pass2:
            messages.error(r, 'Passwords don\'t match!')
            return redirect(vendor_login_page)
        first_name = r.POST.get('first_name')
        last_name = r.POST.get('last_name')
        business_name = r.POST.get('business_name')
        hotel_vendor = models.HotelVendor.objects.create(username=phone_number, first_name=first_name,
                                                         last_name=last_name, email = email, phone_number = phone_number,
                                                          business_name = business_name, email_token=utils.generate_random_token())
        hotel_vendor.set_password(pass1)
        hotel_vendor.save()
        utils.send_vendor_verification_mail(email, hotel_vendor.email_token)
        return redirect(vendor_login_page)
    return render(r, 'vendor/register.html')

@login_required(login_url='vendor-login')
def dashboard(r):
    return render(r, 'vendor/dashboard.html', context={'hotels': models.Hotel.objects.filter(hotel_owner=r.user)})

@login_required(login_url='vendor-login')
def add_hotel(r):
    if r.method == 'POST':
        hotel_name = r.POST.get('hotel_name')
        description = r.POST.get('description')
        amenities = r.POST.getlist('amenities')
        price = r.POST.get('hotel_price')
        offer_price = r.POST.get('offer_price')
        location = r.POST.get('location')
        slug = utils.generate_slug(hotel_name)
        hotel_obj = models.Hotel.objects.create(name=hotel_name, description=description, hotel_price=price,
                                    hotel_offer_price=offer_price, hotel_location=location, hotel_slug=slug,
                                                hotel_owner=models.HotelVendor.objects.get(id=r.user.id))
        for amenity in amenities:
            feature = models.Amenities.objects.get(id=amenity)
            hotel_obj.amenities.add(feature)
        hotel_obj.save()
        messages.success(r, 'Hotel Added Successfully!')
        return redirect(dashboard)
    return render(r, 'vendor/add_hotel.html', context={'amenities': models.Amenities.objects.all()})

@login_required(login_url='vendor-login')
def upload_hotel_images(r, slug):
    hotel_obj = models.Hotel.objects.get(hotel_slug=slug)
    if r.method == 'POST':
        image_name = r.FILES['image']
        models.HotelImages.objects.create(hotel_owner=hotel_obj, image=image_name)
        return HttpResponseRedirect(r.path_info)
    return render(r, 'vendor/upload_images.html', context={'images': models.HotelImages.objects.filter(hotel_owner=hotel_obj)})

@login_required(login_url='vendor-login')
def delete_hotel_image(r, image_id):
    hotel_image = models.HotelImages.objects.get(id=image_id)
    hotel_image.delete()
    messages.success(r, 'Hotel Image Deleted Successfully!')
    return redirect(upload_hotel_images, slug=hotel_image.hotel_owner.hotel_slug)

@login_required(login_url='vendor-login')
def edit_hotel_details(r, slug):
    hotel_obj = models.Hotel.objects.get(hotel_slug=slug)
    if hotel_obj.hotel_owner.id != r.user.id:
        messages.warning(r, 'You are not authorized to edit this hotel!')
        return redirect(dashboard)
    if r.method == 'POST':
        hotel_obj.name = r.POST.get('hotel_name')
        hotel_obj.description = r.POST.get('description')
        hotel_obj.hotel_price = r.POST.get('hotel_price')
        hotel_obj.hotel_offer_price = r.POST.get('offer_price')
        hotel_obj.hotel_location = r.POST.get('location')
        hotel_obj.save()
        messages.success(r, 'Hotel Details Updated Successfully!')
        return HttpResponseRedirect(r.path_info)
    return render(r, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'amenities': models.Amenities.objects.all()})

def check_bookings(r, slug):
    hotel_obj = models.Hotel.objects.get(hotel_slug=slug)
    if hotel_obj.hotel_owner_id != r.user.id:
        messages.warning(r, 'You are not authorized to view this page!')
        return redirect(dashboard)
    return render(r, 'vendor/check_booking.html', context={'bookings': hotel_obj.booked_hotel_name.all()})

def user_check_bookings(r):
    bookings = models.HotelBooking.objects.filter(user=r.user)
    return render(r, 'user/check_booking.html', context={'bookings': bookings})
