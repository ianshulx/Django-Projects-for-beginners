from django.urls import path
from .views import (SignUpView, PatientProfileUpdateView, DoctorProfileUpdateView, 
                    PatientDashboardView, DoctorDashboardView,PatientDetailView, MarkHealthDataReviewedView , 
                    BookDoctorView, SubmitReviewView, SendUserIdToNodeMCUView)
from . import views
from django.views.generic import TemplateView


ap_name = 'registration'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),

    path('patient/profile/', PatientProfileUpdateView.as_view(), name='patient-profile'),
    path('doctor/profile/', DoctorProfileUpdateView.as_view(), name='doctor-profile'),
    path('patient/dashboard/<int:pk>/', PatientDashboardView.as_view(), name = 'patient-dashboard'),
    path('doctor/dashboard/', DoctorDashboardView.as_view(), name = 'doctor-dashboard'),
    path('patient/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('health-data/mark-reviewed/', MarkHealthDataReviewedView.as_view(), name='mark-reviewed'),

    path('book-doctor/',BookDoctorView.as_view(), name='book-doctor'),
    path('submit-review/', SubmitReviewView.as_view(), name='submit-review'),

    path('approval_pending/', TemplateView.as_view(template_name="registration/approval_pending.html"), name='approval_pending'),
 
    path('forgot-password/', views.ForgotPassword, name = 'forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name = 'password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name = 'reset-password'),

    path('send-user-id/', SendUserIdToNodeMCUView.as_view(), name='send_user_id'),
    
]