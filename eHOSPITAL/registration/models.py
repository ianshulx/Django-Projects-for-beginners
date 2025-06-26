from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from datetime import date
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

import random 
import uuid
 

class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='patient')
    user_id = models.CharField(max_length=14, unique=True, blank=True, null=True)
    is_approved = models.BooleanField(default = False)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,blank=True,null=True)
    email = models.EmailField(unique=True)



    def save(self, *args, **kwargs):
        if not self.user_id and self.user_role == 'patient':
            self.user_id = self.generate_unique_user_id()
        super().save(*args, **kwargs)

    def generate_unique_user_id(self):#]
        while True:
            unique_id = str(random.randint(00000000000000, 99999999999999)).zfill(14)  
            if not User.objects.filter(user_id=unique_id).exists():
                return unique_id


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year_of_birth = models.IntegerField(null=True, blank=True, default=2000)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank = True)
    assigned_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Phone Number', blank=True, null=True)


    @property
    def age(self):
        return date.today().year - self.year_of_birth

    def __str__(self):
        return self.user.get_full_name()
    

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50)
    registration_id = models.CharField(max_length=20, unique=True)
    year_of_birth = models.IntegerField(null=True, blank=True, default=2000)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank = True)

    max_patients = models.PositiveBigIntegerField(default=settings.MAX_PATIENTS_PER_DOCTOR)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" #({self.registration_id}) - {self.specialty}
    
    @property
    def age(self):
        return date.today().year - self.year_of_birth
    
    @property
    def current_patients_count(self):
        return self.patient_set.count()
    
    @property
    def can_accept_more_patients(self):
        return self.current_patients_count < self.max_patients and self.is_available
    
    class Meta:
        ordering = ['first_name', 'last_name', 'registration_id', 'specialty']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


#intialize patient health data
@receiver(post_save, sender=Patient)
def create_health_data(sender, instance, created, **kwargs):
    if created:
        PatientHealthData.objects.create(
            patient=instance,
            spo2=97.0,
            temperature=36.2,
            heart_rate=80
        )


class PatientHealthData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_data')
    spo2 = models.FloatField(help_text="Oxygen saturation level (%)")
    temperature = models.FloatField(help_text="Body temperature (°C)")
    heart_rate = models.IntegerField(help_text="Heart rate (bpm)")
    recorded_at = models.DateTimeField(default=now, help_text="Timestamp of the data recorded")
    reviewed_by_doctor = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey('Doctor',on_delete=models.SET_NULL, null = True, blank = True)
    review_comment = models.TextField(null=True, blank=True, help_text="Comment from the doctor after reviewing the health data")
    review_status = models.CharField(max_length=20, choices=(
        ('Normal', 'Normal'),
        ('Fair', 'Fair'),
        ('Critical', 'Critical')),
        blank=True,
        null=True,
    )
 
    def __str__(self):
        return f"{self.patient.user.username} - {self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @property
    def assigned_doctor(self):
        return self.patient.assigned_doctor
    
    class Meta:
        verbose_name = 'Patient Health Data'
        verbose_name_plural = 'Patient Health Data'



class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique = True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and (timezone.now() - self.created_when) < timedelta(minutes=10)

    def __str__(self):
        return f"Password reset for {self.user.username} on {self.created_when.strftime('%Y-%m-%d %H:%M:%S')}"
    