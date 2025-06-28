from django.http import HttpResponseForbidden
from .models import Doctor

class DoctorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            request.doctor = Doctor.objects.get(user=request.user) 
        except Doctor.DoesNotExist:
            return HttpResponseForbidden("Access Denied. You must be a doctor to access this page.")
        return super().dispatch(request, *args, **kwargs)