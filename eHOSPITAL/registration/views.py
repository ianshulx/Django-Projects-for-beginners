from django.shortcuts import render,redirect , get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import login #?
from django.contrib.auth.views import LoginView
from .models import User, Patient, Doctor, PatientHealthData, PasswordReset
from .forms import CustomUserCreationForm, PatientProfileForm, DoctorProfileForm, PasswordResetRequestForm, PasswordResetConfirmForm, HealthDataReviewForm
from django.views import View
import uuid
from django.contrib.auth import get_user_model
from django.http import Http404
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages

from django.urls import reverse
from django.utils import timezone
from django.db import models
#test
import json
from django.http import JsonResponse
# mixins
from .mixins import DoctorRequiredMixin
# for emails
from django.core.mail import send_mail, EmailMessage
from eHospital.settings import EMAIL_HOST_USER

# for decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# search functionality
from django.db.models import Q, Count
from django.urls import reverse

# for password reset
from django.contrib.auth.password_validation import validate_password
import logging
logger = logging.getLogger(__name__)


class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'This email is already in use.')
            return self.form_invalid(form)
        
        user = form.save()
        login(self.request, user)
    
        if user.user_role == 'patient':
            print('Patient User')
            return redirect(reverse_lazy('registration:patient-profile'))
        
        elif user.user_role == 'doctor':
            print('Daktari')
            doctor_email = user.email
            doctor_username = user.username
            admin_email = settings.ADMIN_EMAIL

            try:
                send_mail(
                    subject = 'New Doctor Registration Pending Approval',
                    message = (
                        f"A new doctor has registered:\n\n"
                        f"Username: {doctor_username}\n"
                        f"Email: {doctor_email}\n\n"
                        f"Please review and approve this account in the admin panel."
                    ),
                    from_email = EMAIL_HOST_USER,
                    recipient_list = [admin_email],
                    fail_silently = False,
                )
                print('Email sent to admin for approval')

            except Exception as e:
                 print(f'Failed to send email: {e}')

            user.is_approved = False
            user.save()
            return redirect(reverse_lazy('registration:approval_pending'))
        else:
            return redirect('home')


class PatientProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Patient
    form_class = PatientProfileForm
    template_name = 'registration/patient_profile.html'
    
    def get_success_url(self):
        return reverse_lazy('registration:patient-dashboard', kwargs={'pk': self.request.user.patient.pk})

    def get_object(self):
        return Patient.objects.get_or_create(user=self.request.user)[0]


class DoctorProfileUpdateView(UpdateView, DoctorRequiredMixin):
    model = Doctor
    form_class = DoctorProfileForm
    template_name = 'registration/doctor_profile.html'
    success_url = reverse_lazy('registration:doctor-dashboard')

    def get_object(self):
        return Doctor.objects.get_or_create(user=self.request.user)[0]


class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/patient_dashboard_1.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'], user=self.request.user)
       

        latest_health_data = (
            PatientHealthData.objects.filter(patient=patient).order_by('-recorded_at').first() 
        )

        recent_health_data = (PatientHealthData.objects.filter(patient=patient).order_by('-recorded_at')[:50])

        chart_data = {
            "timestamps": [data.recorded_at.strftime("%H:%M:%S") for data in recent_health_data],
            "heart_rates": [data.heart_rate for data in recent_health_data],
            "spo2_levels": [data.spo2 for data in recent_health_data],
            "temperatures": [data.temperature for data in recent_health_data],
        }
        reviewed_data = PatientHealthData.objects.filter(patient=patient,reviewed_by_doctor__isnull=False).order_by('-reviewed_at')

        context['chart_data'] = chart_data
        context['reviewed_data'] = reviewed_data
        context['patient'] = patient
        context['latest_health_data'] = latest_health_data
        context['recent_health_data'] = recent_health_data
        return context


class DoctorDashboardView(LoginRequiredMixin, DoctorRequiredMixin,ListView):
    model = Patient
    template_name = 'registration/doctor_dashboard_test2.html'
    context_object_name = 'patients'

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        # Filter patients assigned to the logged-in doctor
        return Patient.objects.filter(assigned_doctor=doctor).prefetch_related(
            models.Prefetch('health_data',
                queryset=PatientHealthData.objects.order_by('-recorded_at'),
                to_attr='recent_health_data'
            )
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class PatientDetailView(LoginRequiredMixin, DoctorRequiredMixin, DetailView):
    model = Patient
    template_name = 'registration/patient_detail2.html'
    context_object_name = 'patient'

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Patient.objects.filter(assigned_doctor=doctor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        health_data = patient.health_data.order_by('-recorded_at')
        context['health_data'] = health_data
        context['review_form'] = HealthDataReviewForm()
        return context


    # email functionality
    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                patient = self.get_object()
                doctor = Doctor.objects.get(user=request.user)
                
                # Get email data from request
                data = json.loads(request.body)
                consultation_date = data.get('consultation_date')
                consultation_time = data.get('consultation_time')
                message_body = data.get('message', '')
                
                # Generate meet link (you can customize this based on your video platform)
                meet_link = f"https://meet.google.com/ojj-swyk-syg "  
                
                # Email subject and content
                subject = f"Consultation Request from Dr. {doctor.first_name} {doctor.last_name}"
                
                email_message = f"""
                Dear {patient.first_name} {patient.last_name},

                Dr. {doctor.first_name} {doctor.last_name} has requested a video consultation with you.

                Consultation Details:
                - Date: {consultation_date} 
                - Time: {consultation_time} HOURS
                - Video Call Link: {meet_link}

                Additional Message:
                {message_body}

                Please join the video call at the scheduled time using the link above.

                If you need to reschedule, please contact our office.

                Best regards,
                Medical Team
                """

                send_mail(
                    subject=subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[patient.user.email],
                    fail_silently=False,
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Consultation email sent successfully!'
                })
                
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Failed to send email: {str(e)}'
                })
        return super().post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MarkHealthDataReviewedView(View): 

    
    def post(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=request.user)
        patient_id = request.POST.get('patient_id')
        data_id = request.POST.get('data_id')
        review_comment = request.POST.get('review_comment', '').strip()
        review_status = request.POST.get('review_status')
        
        # Get the patient (ensure they're assigned to this doctor)
        patient = get_object_or_404(Patient, id=patient_id, assigned_doctor=doctor)
        
        if data_id == 'all':
            # Mark all unreviewed data for this patient as reviewed
            updated_count = patient.health_data.filter(
                reviewed_by_doctor=False
            ).update(
                reviewed_by_doctor=True,
                reviewed_at=timezone.now(),
                reviewed_by=doctor
            )
            return JsonResponse({
                'status': 'success',
                'message': f'Marked {updated_count} records as reviewed'
            })
        else:
            health_data = get_object_or_404(
                PatientHealthData, 
                id=data_id, 
                patient=patient,
                reviewed_by_doctor=False 
            )

            health_data.reviewed_by_doctor = True
            health_data.reviewed_at = timezone.now()
            health_data.reviewed_by = doctor

            if review_comment:
                health_data.review_comment = review_comment
            if review_status:
                health_data.review_status = review_status

            health_data.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Health data marked as reviewed',
                'review_details': {
                    'reviewed_at': health_data.reviewed_at.strftime("%Y-%m-%d %H:%M"),
                    'doctor': f"Dr. {doctor.user.get_full_name()}",
                    'comment': health_data.review_comment,
                    'status': health_data.get_review_status_display()
                }
            })

  

class BookDoctorView(LoginRequiredMixin,ListView):
    template_name = 'registration/book_doctor.html'
    model = Doctor
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        #get doctors whi have less than their max_patients 
        queryset = Doctor.objects.annotate(patient_count = Count('patients')).filter(patient_count__lt = models.F('max_patients')) 
        #get search query
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            #split the search query into words
            search_words = search_query.split()
            #create Q objects for different search combinations
            search_filter = Q()

            for word in search_words:
                word_filter = (
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(specialty__icontains=word)
                )
                search_filter |= word_filter
            #search for full name combinations
            search_filter |=(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(specialty__icontains=search_query)
            )
            queryset = queryset.filter(search_filter)
        return queryset.distinct().order_by('first_name', 'last_name')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        # Get current patient
        try:
            patient = Patient.objects.get(user=self.request.user)
            context['current_patient'] = patient
            context['has_assigned_doctor'] = patient.assigned_doctor is not None
        except Patient.DoesNotExist:
            context['current_patient'] = None
            context['has_assigned_doctor'] = False
            
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle doctor selection
        doctor_id = request.POST.get('doctor_id')
        
        if not doctor_id:
            messages.error(request, 'Please select a doctor.')
            return redirect('book_doctor')
        
        try:
            # Get the patient
            patient = Patient.objects.get(user=request.user)
            
            # Get the selected doctor
            doctor = get_object_or_404(Doctor, id=doctor_id)
            
            # Check if doctor still has capacity
            current_patient_count = Patient.objects.filter(assigned_doctor=doctor).count()
            if current_patient_count >= doctor.max_patients:
                messages.error(request, f'Dr. {doctor.first_name} {doctor.last_name} is currently at full capacity.')
                return redirect('book_doctor')
            
            # Assign the doctor to the patient
            patient.assigned_doctor = doctor
            patient.save()
            
            messages.success(request, f'Successfully booked Dr. {doctor.first_name} {doctor.last_name} as your assigned doctor!')
            return redirect('registration:book-doctor')  # Redirect to patient dashboard
            
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found. Please complete your profile first.')
            return redirect('registration:patient-profile')
        """
        except Exception as e:
            messages.error(request, 'An error occurred while booking the doctor. Please try again.')
            return redirect('registration:book-doctor')
    """


    
class SubmitReviewView(LoginRequiredMixin, DoctorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Ensure the user is a doctor
        if not hasattr(request.user, 'doctor'):
            return JsonResponse({
                'status': 'error',
                'message': 'Only doctors can submit reviews'
            }, status=403)
        
        # Get the data from the POST request
        patient_id = request.POST.get('patient_id')
        data_id = request.POST.get('data_id')
        status = request.POST.get('status')
        comment = request.POST.get('comment', '')
        
        try:
            # Get the health data record
            health_data = PatientHealthData.objects.get(
                id=data_id,
                patient__user_id=patient_id
            )
            # Update the record with review information
            health_data.reviewed_by_doctor = request.user.doctor
            health_data.reviewed_at = timezone.now()
            health_data.review_status = status
            health_data.review_comment = comment
            health_data.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Review submitted successfully'
            })
            
        except PatientHealthData.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Health data record not found'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
 

def ForgotPassword(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                existing_reset = PasswordReset.objects.filter(
                    user=user, 
                    created_when__gte=timezone.now() - timezone.timedelta(minutes=5)
                ).first()
                
                if existing_reset:
                    messages.error(request, 'A password reset was already sent recently. Please check your email.')
                    return redirect('registration:forgot-password')
                
                PasswordReset.objects.filter(user=user).delete() 
                new_password_reset = PasswordReset(user=user)
                new_password_reset.save()

                password_reset_url = reverse('registration:reset-password', kwargs={'reset_id': new_password_reset.reset_id})
                full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
                full_password_reset_url2= f'https://63167tl1-8000.uks1.devtunnels.ms{password_reset_url}'

                email_body = f'''Hello {user.get_full_name() or user.username},

You requested a password reset for your account. Click the link below to reset your password:

{full_password_reset_url}

or click on this link:

{full_password_reset_url2}

This link will expire in 10 minutes.

If you didn't request this reset, please ignore this email.

EHMS Team'''
                
                try:
                    email_message = EmailMessage(
                        'Reset your password',
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [email]
                    )
                    email_message.send()
                    logger.info(f"Password reset email sent to {email}")
                except Exception as e:
                    logger.error(f"Failed to send password reset email to {email}: {str(e)}")
                    messages.error(request, 'Failed to send reset email. Please try again later.')
                    return redirect('registration:forgot-password')
                
                return redirect('registration:password-reset-sent', reset_id=new_password_reset.reset_id)
            
            except User.DoesNotExist:
                # This shouldn't happen because form validation already checked the email exists
                logger.warning(f"Password reset attempt for non-existent email: {email}")
                messages.error(request, 'If an account with that email exists, a password reset link has been sent.')
                return redirect('registration:forgot-password')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'registration/forgot_password.html', {'form': form})


def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'registration/password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset link')
        return redirect('registration:forgot-password')


def ResetPassword(request, reset_id):
    try:
        password_reset = get_object_or_404(PasswordReset, reset_id=reset_id)

        expiration_time = password_reset.created_when + timezone.timedelta(minutes=10)
        if timezone.now() > expiration_time:
            password_reset.delete()
            messages.error(request, 'This password reset link has expired. Please request a new one.')
            return redirect('registration:forgot-password')
        
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
             
            if not password or not confirm_password:
                messages.error(request, 'Both password fields are required.')
                return render(request, 'registration:reset-password', {'reset_id': reset_id})
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'registration/reset_password.html', {'reset_id': reset_id})
            
            try:
                validate_password(password, user=password_reset.user)
            except Exception as e:
                for error in e.messages:
                    messages.error(request, error)
                    return render(request, 'registration/reset_password.html', {'reset_id': reset_id})
                
            if  timezone.now() > expiration_time:
                password_reset.delete()
                messages.error(request, 'This password reset link has expired. Please request a new one.')
                return redirect('registration:forgot-password')
            # Update the user's password
            user = password_reset.user
            user.set_password(password)
            user.save()

            password_reset.delete()

            logger.info(f"Password reset successful for user: {user.email}")
            messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
            redirect('login')
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid or expired reset link')
        return redirect('registration:forgot-password')
    
    return render(request, 'registration/reset_password.html')



class SendUserIdToNodeMCUView(LoginRequiredMixin, View):
    """
    View that sends the logged-in user's ID to the NodeMCU device
    when triggered by a button click.
    """
    
    def post(self, request, *args, **kwargs):
        # Get the logged-in user's ID
        user_id = request.user.id
        
        # NodeMCU server details from settings (you should add these to your settings.py)
        node_mcu_url = getattr(settings, 'NODE_MCU_SERVER', 'http://192.168.0.23:8000')
        endpoint = getattr(settings, 'NODE_MCU_USER_ID_ENDPOINT', '/update-user-id/')
        
        # Prepare the payload
        payload = {
            'user_id': user_id
        }
        
        try:
            # Send the request to NodeMCU
            response = requests.post(
                f"{node_mcu_url}{endpoint}",
                json=payload,
                timeout=5  # 5 second timeout
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                return JsonResponse({
                    'status': 'success',
                    'message': f'User ID {user_id} sent successfully to NodeMCU'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'NodeMCU responded with status code {response.status_code}'
                }, status=400)
                
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Failed to communicate with NodeMCU: {str(e)}'
            }, status=500)