
from django.shortcuts import render, redirect , HttpResponse , HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Vehicle_details, Trip
import uuid
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .helpers import send_forget_email
from django.contrib.auth import logout

from django.urls import reverse
from django.http import FileResponse 

from .forms import VehicleForm, TripForm

from datetime import datetime

# Get the current date
current_date = datetime.now().date()

import pytz

def get_current_datetime(timezone_str):
    # Get the timezone object based on the timezone string
    timezone = pytz.timezone(timezone_str)
    # Get the current date and time in UTC
    utc_now = datetime.utcnow()
    # Convert the UTC time to the specified timezone
    local_datetime = utc_now.replace(tzinfo=pytz.utc).astimezone(timezone)
    # Format the date and time as a string
    formatted_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_datetime

# Example usage
timezone_str = 'Asia/Kolkata'  # Replace with your desired timezone
current_datetime = get_current_datetime(timezone_str)



import csv
import json


from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO




#! For Emails -----------------------------------------------------------------------------------------

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#? To download files -----------------------------------------------------------------------------------

from django.http import FileResponse, Http404

from datetime import datetime
 

def password_checker(password):
    if len(password) < 8:
        return f"Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    return True


# Create your views here.

def unpaid(username):
    pdf_dir = os.path.join(settings.MEDIA_ROOT[0], username)  # Use the specific folder
    pdf_files = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(pdf_dir, filename)
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
            pdf_files.append({'name': filename, 'creation_date': creation_date})
    return pdf_files

def paid(username):
    username = f"{username}_paid"
    pdf_dir = os.path.join(settings.MEDIA_ROOT[0], username)  # Use the specific folder
    paid_pdf_files = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(pdf_dir, filename)
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
            paid_pdf_files.append({'name': filename, 'creation_date': creation_date})
    return paid_pdf_files


# def pricing(request, username):
#     paid_files = paid(username)
#     unpaid_files = unpaid(username)
#     pdf_dir = os.path.join(settings.MEDIA_ROOT[0], username)  # Use the specific folder
#     pdf_files = []
#     for filename in os.listdir(pdf_dir):
#         if filename.endswith('.pdf'):
#             file_path = os.path.join(pdf_dir, filename)
#             creation_time = os.path.getctime(file_path)
#             creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
#             pdf_files.append({'name': filename, 'creation_date': creation_date})
#     context = {'pdf_files': pdf_files}
#     return render(request, 'authrization/pricing.html', context)


def pricing(request, username):
    create_folder_in_media(username)
    create_folder_in_media_paid(username)
    paid_files = paid(username)
    unpaid_files = unpaid(username)    
    context = {'paid_files': paid_files, 'unpaid_files': unpaid_files}
    return render(request, 'authrization/pricing.html', context)

def enquiry(request, username):
    
    return render(request, 'authrization/enquiry.html')

def index(request):
    return render(request, 'index.html')



#? ------------------------------- Authentication -------------------------------------------------- ?# 


#! ------------------------------- Login and Register -------------------------------------------------- !# 
# def login_attempt(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
        
#         user = User.objects.filter(username=username).first()
#         email = User.objects.filter(email=username).first()
        
#         if user is None:
#             messages.error(request, 'User not found.')
#             return redirect('login_attempt')
        
#         profile_obj = Profile.objects.filter(user=user).first()
        
#         if profile_obj is not None and profile_obj.isverified:
#             if user.check_password(password):
#                 login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                 messages.success(request, 'Login successful.')
#                 return redirect('/')
#             else:
#                 messages.error(request, 'Password is incorrect.')
#                 return redirect('login_attempt')
        
#         user = authenticate(username=username, password=password)
#         if user is None:
#             messages.error(request, 'Password is incorrect.')
#             return redirect('login_attempt')
        
#         login(request, user,backend='django.contrib.auth.backends.ModelBackend')
#         messages.success(request, 'Login successful.')
#         return redirect('/')
        
#     return render(request, 'authrization/login.html')


def login_attempt(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if a user with the given email exists
        user = User.objects.filter(email=email).first()
        
        if user is None:
            messages.error(request, 'User not found.')
            return redirect('login_attempt')
        
        # Assuming Profile is related to User through a OneToOneField or ForeignKey
        profile_obj = Profile.objects.filter(user=user).first()
        
        if profile_obj is not None and profile_obj.isverified:
            if user.check_password(password):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Login successful.')
                return redirect('/')
            else:
                messages.error(request, 'Password is incorrect.')
                return redirect('login_attempt')
        
        # Authenticate user using email and password
        user = authenticate(request, username=user.username, password=password)
        if user is None:
            messages.error(request, 'Password is incorrect.')
            return redirect('login_attempt')
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Login successful.')
        return redirect('/')
        
    return render(request, 'authrization/login.html')

def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if password_checker(password) != True:
            messages.error(request, password_checker(password))
            return redirect('register_attempt')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register_attempt')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('register_attempt')

        try:
            user_obj = User.objects.create_user(username=username, email=email, password=password)
            profile_obj = Profile.objects.create(user=user_obj, auth_token=str(uuid.uuid4()), isverified=False)

            send_mail_after_registration(email, profile_obj.auth_token)

            create_folder_in_media(username)
            create_folder_in_media_paid(username)
            messages.success(request, 'Registration successful. Please check your email to verify your account.')
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred during registration.')
            return redirect('register_attempt')

    return render(request, 'authrization/register.html')


def logout_attempt(request):
    
    print(f'Login out {request.user}')
    messages.success(request, 'Logout successful.')
    logout(request)
    print(request.user)
    return HttpResponseRedirect('/')


#! ------------------------------- Email Verification -------------------------------------------------- !# 

# def send_mail_after_registration(email, token):
#     subject = 'Your account needs to be verified'
#     message = f'Hi, please use the following link to verify your account: http://127.0.0.1:8000/authrization/verify/{token}'
    
#     email_from = 'sharmaji8991mayank@gmail.com'
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)
    
    

# def send_mail_after_registration(email, token):
#     subject = 'Your account needs to be verified'
    
#     html_message = render_to_string('authrization/verification_email.html', {'token': token})
#     from_email = 'mayank@gmail.com'
#     recipient_list = [email]
    
#     message = strip_tags(html_message)
    
#     email = EmailMessage(subject=subject, body=html_message, from_email=from_email, to=recipient_list)
#     email.content_subtype = 'html'
#     email.send()
    
    
def send_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    
    html_message = render_to_string('authrization/verification_email.html', {'token': token})
    from_email = 'admin@demomailtrap.com'
    # recipient_list = [email]
    recipient_list = ('jilat13045@kernuo.com',)
    
    
    message = strip_tags(html_message)
    
    email = EmailMessage(subject=subject, body=html_message, from_email=from_email, to=recipient_list)
    email.content_subtype = 'html'
    email.send()
    


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.isverified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login_attempt')
            profile_obj.isverified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login_attempt')
        else:
            return redirect('error_page')
    except Exception as e:
        print(e)
        return redirect('error_page')




#! ------------------------------- Forget Password -------------------------------------------------- ?# 

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        profile_obj = Profile.objects.filter(user__email=email).first()
        if profile_obj:
            token = str(uuid.uuid4())
            profile_obj.auth_token = token
            profile_obj.save()
            send_forget_email(email, token)  # Send email with reset link
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('forget_password')
        else:
            messages.error(request, 'No user found with that email address.')
    
    return render(request, 'authrization/forget_password.html')
   

def change_password(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if request.method == 'POST':
                password = request.POST.get('password')
                profile_obj.user.set_password(password)
                profile_obj.user.save()
                messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('login_attempt')
            else:
                return render(request, 'authrization/change_password.html')
        else:
            messages.error(request, 'Invalid token. Please try again.')
            return redirect('error_page')
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again.')
    
    return redirect('error_page')



def error_page(request):
    return render(request, 'authrization/error.html')


#! ------------------------------- Vehicle Details -------------------------------------------------- ?# 
@login_required
def vehicle_details(request, username):
    # profile = get_object_or_404(Profile, user__username=username)
    # profile = Profile.objects.filter(user__username=username).first()
    profile = get_object_or_404(Profile, user__username=username)
    print(f"Retrieved Profile: {profile}")  # Debugging statement
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            print('Form validated')
            vehicle_detail = form.save(commit=False)
            vehicle_detail.user = profile  # Assign the profile object directly
            vehicle_detail.save()
            for i, j in form.cleaned_data.items():
                print(f"{i} : {j}")
            
            return redirect('vehicle_details', username=username)  # Assuming you want to redirect back to the same page
    else:
        form = VehicleForm()
        
    vehicle_detail = Vehicle_details.objects.filter(user=profile)
    print(vehicle_detail)
    # return render(request, 'authrization/vehicle_details.html', {'form': form, 'vehicle_details': vehicle_detail, 'username':username})
    return render(request, 'authrization/tables.html', {'form': form, 'vehicle_details': vehicle_detail, 'username':username})

def Add_vehicle(request, username):

    profile = get_object_or_404(Profile, user__username=username)
    print(f"Retrieved Profile: {profile}")  # Debugging statement
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            print('Form validated')
            vehicle_detail = form.save(commit=False)
            vehicle_detail.user = profile  # Assign the profile object directly
            vehicle_detail.save()
            for i, j in form.cleaned_data.items():
                print(f"{i} : {j}")
            messages.success(request, 'Your vehicle added successfully.')
            return redirect('Add_vehicle', username=username)  # Assuming you want to redirect back to the same page
    else:
        form = VehicleForm()
        
    vehicle_detail = Vehicle_details.objects.filter(user=profile)
    print(vehicle_detail)
    return render(request, 'authrization/Add_vehicle.html', {'form': form, 'vehicle_details': vehicle_detail, 'username':username})


def delete_vehicle(request, username, vehicle_number):
    # Get the profile associated with the username
    profile = Profile.objects.filter(user__username=username).first()
    if profile:
        # Get the vehicle details associated with the user and the specific vehicle number
        vehicle_to_delete = get_object_or_404(Vehicle_details, user=profile, vehicle_number=vehicle_number)
        # Delete the specific vehicle
        
        vehicle_to_delete.delete()
        messages.success(request, 'Your vehicle deleted successfully.')

    # Redirect back to the same page
    return redirect('vehicle_details', username=username)




#! ------------------------------------- Extra -------------------------------------------------- ?#

#? Download pdf file


# def index(request):
#     pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_files')  # Use the specific folder
#     pdf_files = []
#     for filename in os.listdir(pdf_dir):
#         if filename.endswith('.pdf'):
#             file_path = os.path.join(pdf_dir, filename)
#             creation_time = os.path.getctime(file_path)
#             creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
#             pdf_files.append({'name': filename, 'creation_date': creation_date})
#     context = {'pdf_files': pdf_files}
#     return render(request, 'index.html', context)


#? To download the files from the server  

def download_pdf(request, filename, username):
    file_path = os.path.join(settings.MEDIA_ROOT[0], username, filename)  # Use the specific folder
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        raise Http404


 

def create_folder_in_media(folder_name):
    folder_path = os.path.join(settings.MEDIA_ROOT[0], folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # return f"Folder '{folder_name}' created successfully."
        return folder_name
    else:
        return f"Folder '{folder_name}' already exists."

def create_folder_in_media_paid(folder_name):
    folder_name = f"{folder_name}_paid"
    folder_path = os.path.join(settings.MEDIA_ROOT[0], folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # return f"Folder '{folder_name}' created successfully."
        return folder_name
    


#? ------------------------------- Trip -------------------------------------------------- ?#
from .DataAnalysis import DataAnalysisuser,Total_Journey_Distance





#? Generate Invoice 
def extract_data(uuid_field_value):
    trip = Trip.objects.get(uuid_field=uuid_field_value)
    filename = filename = f'{uuid_field_value}.csv'
    filepath = os.path.join(settings.MEDIA_ROOT[1], filename)
    highwaypath = os.path.join(settings.MEDIA_ROOT[1], 'highway.geojson')
    DataAnalysisuser(highwaypath, filepath)
    Total_Distance = Total_Journey_Distance(trip.starting_point, trip.ending_point)
    Usertotaldistance, Usertotaltime, EachHighwayDistance, Total_km_on_highway, Average_speed, vehicle_number = DataAnalysisuser(highwaypath, filepath)
    TRIP = {
        'uuid_field': trip.uuid_field,
        'starting_point': trip.starting_point,
        'ending_point': trip.ending_point,
        'vehicle_number': trip.vehicle_number,
        'vehicle_type': trip.vehicle_type,
        'total_km': str(Total_Distance),
        'total_amount': str((Decimal(Total_km_on_highway)*trip.charge_per_km).toprec(3)),
        'charge_per_km': str(trip.charge_per_km),
        'Usertotaldistance': Usertotaldistance,
        'Usertotaltime': Usertotaltime,
        'EachHighwayDistance': EachHighwayDistance,
        'Total_km_on_highway': Total_km_on_highway,
        'Average_speed': Average_speed,
        'vehicle_number': vehicle_number,
        'Date' : str(current_date)
        
    }
    
    instance = get_object_or_404(Trip, uuid_field=uuid_field_value)
    instance.total_km = TRIP['total_km']
    instance.total_amount = TRIP['total_amount']
    instance.destination_reached_time = get_current_datetime('Asia/Kolkata')
    instance.save()
    
    
    
    return TRIP
    





# def invoice(request, uuid_field_value):
#     trip = Trip.objects.get(uuid_field=uuid_field_value)
#     filename = filename = f'{uuid_field_value}.csv'
#     filepath = os.path.join(settings.MEDIA_ROOT[1], filename)
#     highwaypath = os.path.join(settings.MEDIA_ROOT[1], 'highway.geojson')
#     print('--------------------------------------------------------------')
#     DataAnalysisuser(highwaypath, filepath)
#     Total_Distance = Total_Journey_Distance(trip.starting_point, trip.ending_point)
#     Usertotaldistance, Usertotaltime, EachHighwayDistance, Total_km_on_highway, Average_speed = DataAnalysisuser(highwaypath, filepath)
#     print('--------------------------------------------------------------')
#     print(f"Trip: {trip}")
#     TRIP = {
#         'uuid_field': trip.uuid_field,
#         'starting_point': trip.starting_point,
#         'ending_point': trip.ending_point,
#         'vehicle_number': trip.vehicle_number,
#         'vehicle_type': trip.vehicle_type,
#         'total_km': Total_Distance,
#         'total_amount': trip.total_amount,
#         'charge_per_km': trip.charge_per_km,
#         'Usertotaldistance': Usertotaldistance,
#         'Usertotaltime': Usertotaltime,
#         'EachHighwayDistance': EachHighwayDistance,
#         'Total_km_on_highway': Total_km_on_highway,
#         'Average_speed': Average_speed
#     }
#     return render(request, 'Trip/invoice.html', context = TRIP)


def generate_pdf(request, username, uuid_field_value):
    create_folder_in_media_paid(username)   # Create a folder for paid invoices
    pdf_file_path, error = generate_and_save_pdf(username, uuid_field_value)
    TRIP = extract_data(uuid_field_value)
    
    request.session['TRIP'] = TRIP
    
    instance = get_object_or_404(Trip, uuid_field=uuid_field_value)
    instance.total_km = TRIP['total_km']
    instance.total_amount = TRIP['total_amount']
    instance.destination_reached_time = get_current_datetime('Asia/Kolkata')
    instance.save()
    if error:
        return HttpResponse(error)
    
    return HttpResponseRedirect(reverse('invoice'))

def invoice(request):
    TRIP = request.session.get('TRIP', {})
    print(f"TRIP in invoice: {TRIP}")
    return render(request, 'Trip/invoice.html', context=TRIP)

def bill_calculation(vehicle_type,total_km):
    if vehicle_type == 'CAR':
        per_km = 0.4
        return float(total_km) * 0.4, per_km
    elif vehicle_type == 'TRUCK':
        per_km = 0.8
        return float(total_km)*0.8, per_km
    elif vehicle_type == 'BUS':
        per_km = 0.6
        return float(total_km)*0.6, per_km
    elif vehicle_type == 'BIKE':
        per_km = 0.2
        return float(total_km)*0.2, per_km   
    else:
        return float(total_km)*1, 1




from django.shortcuts import render, HttpResponseRedirect
def Trips_fun(request):
    if request.method == 'POST':
        form = TripForm(request.POST, user=request.user)
        if form.is_valid():
            starting_point = form.cleaned_data.get('starting_point')
            ending_point = form.cleaned_data.get('ending_point')
            vehicle_number = form.cleaned_data.get('vehicle_number')
            uuid_field = form.cleaned_data.get('uuid_field')
            print(f"UUID in view.py : {uuid_field}")
            uniq_uuid = uuid_field
        
            try:
                # Retrieve the vehicle instance from the database
                vehicle = Vehicle_details.objects.get(vehicle_number=vehicle_number)
                
                # Assign the retrieved vehicle instance to form.instance
                form.instance.vehicle_number = vehicle
                
                # Access vehicle_type from the retrieved vehicle and assign it to form.instance
                form.instance.vehicle_type = vehicle.vehicle_type.upper()
                vehicle_type = vehicle.vehicle_type.upper()
                form.instance.total_km = Total_Journey_Distance(starting_point, ending_point)
                datetime_str = get_current_datetime('Asia/Kolkata')
                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                form.instance.date_entered = datetime_obj                          
                form.instance.total_amount,form.instance.charge_per_km =  bill_calculation(str(vehicle_type), form.instance.total_km)
                
                
                # Save the form to create a Trip object
                trip = form.save()
                
                print(f"Starting Point: {starting_point}")
                print(f"Ending Point: {ending_point}")
                print(f"Vehicle Number: {vehicle_number}")
                print(f"Vehicle found: {vehicle}")
                print(f"Vehicle Type: {vehicle.vehicle_type}")  # Access vehicle_type from the retrieved vehicle
                print(f"Vehicle Type: {vehicle.vehicle_type}")  # Access vehicle_type from the retrieved vehicle
                
                filename = f'{starting_point}_{ending_point}.csv'
                
                return HttpResponseRedirect(f"{reverse('simulation', args=[filename])}?uniq_uuid={uniq_uuid}")
                
                # return render(request, 'Trip/simulation.html', {'trip': trip})
            
            except Vehicle_details.DoesNotExist:
                print(f"No vehicle found with number {vehicle_number}")
                # Handle case where vehicle_number does not exist in database
                # You might want to add some error handling or redirect here
            
        else:
            print(form.errors)
            # Handle form errors if needed
    
    else:
        my_uuid = uuid.uuid4().hex[:10].upper()  # Generate and shorten UUID
        initial_data = {'uuid_field': my_uuid}
        form = TripForm(initial=initial_data, user=request.user)
    return render(request, 'Trip/desti_form.html', {'form': form})




def simulation(request, filename):
    uniq_uuid = request.GET.get('uniq_uuid')
 
    print(f"UUID in simulation: {uniq_uuid}")
    trip  = Trip.objects.get(uuid_field=uniq_uuid)
    return render(request, 'Trip/simulation.html', {'filename': filename, 'uniq_uuid':uniq_uuid, 'trip': trip})


@csrf_exempt
def get_coordinates(request, filename):
    filepath = os.path.join(settings.STATICFILES_DIRS[1], filename)
    print(filepath)
    coordinates = []
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
                    print(row)
                    if row == ['latitude', 'longitude']:
                        continue
                    else:
                        print(row)
                        lat, lng = map(float, row)
                        coordinates.append({'lat': lat, 'lng': lng})
    return JsonResponse(coordinates, safe=False)

# @csrf_exempt
# def store_coordinate(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         lat = data.get('lat')
#         lng = data.get('lng')
#         print(f"Latitude: {lat}, Longitude: {lng}")
#         filepath = os.path.join(settings.MEDIA_ROOT, 'stored_coordinates.csv')
#         with open(filepath, 'a') as f:
#             writer = csv.writer(f)
#             writer.writerow([lat, lng])
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'failed'}, status=400)

@csrf_exempt
def store_coordinate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # lat = data.get('lat')
        # lng = data.get('lng')
        lat = data['lat']
        lng = data['lng']
        timestamp = data['timestamp']
        vehicle_number = data['vehicleNumber']
        uniq_uuid = data['uniq_uuid']
        print(username(uniq_uuid))
        print(f"Latitude: {lat}, Longitude: {lng} Timestamp: {timestamp} Vehicle Number: {vehicle_number} uuiq_uniq : {uniq_uuid}")
        filename = f'{uniq_uuid}.csv'
        filepath = os.path.join(settings.MEDIA_ROOT[1], filename) 
        
        # Check if the file exists and is empty
        file_exists = os.path.isfile(filepath)
        is_empty = not os.path.getsize(filepath) if file_exists else True
        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            # Write header if the file is empty
            if is_empty:
                writer.writerow(['latitude', 'longitude','VehicleID','Timestamp'])
            writer.writerow([lat, lng, vehicle_number, timestamp])
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def username(uuid):
    trip = Trip.objects.get(uuid_field=uuid)
    return trip.vehicle_number.user.user.username


    
    
    
    
    
    
def generate_and_save_pdf(username, uuid_field_value):
    # Construct template path
    template_path = 'Trip/invoice_pdf.html'
    
    # Render template
    template = get_template(template_path)
    TRIP = extract_data(uuid_field_value)
    trip_id = TRIP['uuid_field']
    vehicle_number = TRIP['vehicle_number']
    filename = f'{trip_id}_{vehicle_number}.pdf'
    
    
      # Add context data
    html = template.render(TRIP)

    # Create a PDF
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result, encoding='utf-8')

    # Check for errors
    if pisa_status.err:
        return None, 'We had some errors <pre>' + html + '</pre>'

    # Save the PDF to a file
    pdf_output = result.getvalue()
    pdf_file_path = os.path.join(settings.MEDIA_ROOT[0],  filename)
    os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)  # Ensure the directory exists
    with open(pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(pdf_output)
    move_file_to_user_folder(filename, username)
    return pdf_file_path, None





import os


def move_file_to_user_folder(filename, username):
    # Define paths
    media_root = settings.MEDIA_ROOT[0]
    source_path = os.path.join(media_root, filename)
    destination_folder = os.path.join(media_root, username)

    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Construct the destination path
    destination_path = os.path.join(destination_folder, filename)

    try:
        # Perform the move operation
        os.replace(source_path, destination_path)
        print(f"File '{filename}' moved to '{destination_folder}' successfully.")
        return True
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return False
    except Exception as e:
        print(f"Error moving file '{filename}': {str(e)}")
        return False


def pay_now(request, username, filename):
    return render(request, 'Trip/pay.html', {'filename': filename, 'username': username})




def move_file_to_paid_folder(filename, username):
    # Define paths
    media_root = settings.MEDIA_ROOT[0]
    source_path = os.path.join(media_root, username, filename)
    username = f"{username}_paid"
    destination_folder = os.path.join(media_root, username)

    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Construct the destination path
    destination_path = os.path.join(destination_folder, filename)

    try:
        # Perform the move operation
        os.replace(source_path, destination_path)
        print(f"File '{filename}' moved to '{destination_folder}' successfully.")
        return True
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return False
    except Exception as e:
        print(f"Error moving file '{filename}': {str(e)}")
        return False



def paybill(request, username, filename):
    move_file_to_paid_folder(filename, username)
    messages.success(request, 'Payment successful.')
    return redirect('pricing', username=username)
    
    
    
    

