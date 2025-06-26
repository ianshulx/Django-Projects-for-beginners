from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor, PatientHealthData
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


User= User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_role','gender']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError("This email is already in use. Please use a different email.")
            return email


class PatientProfileForm(forms.ModelForm):
    user_id = forms.CharField(disabled=True, required=False, label="User ID") 
    age = forms.IntegerField(required=False, disabled=True) 
    gender = forms.CharField(disabled=True, required=False, label='Gender')

    class Meta:
        model = Patient
        fields = ['first_name','last_name', 'year_of_birth','phone_number', 'gender'] 

    def __init__(self, *args, **kwargs):
        super(PatientProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if instance exists (editing an existing profile)
            self.fields['user_id'].initial = self.instance.user.user_id  
            self.fields['first_name'].disabled = False
            self.fields['last_name'].disabled = False
            self.fields['year_of_birth'].required = True
            self.fields['phone_number'].required = True
            self.fields['year_of_birth'].disabled = False
            self.initial['age'] = self.instance.age

            # set gender diplay value
            if hasattr(self.instance.user, 'gender') and self.instance.user.gender:
                if self.instance.user.gender == 'M':
                    self.fields['gender'].initial = 'Male'
                elif self.instance.user.gender == 'F':
                    self.fields['gender'].initial = 'Female'
                else:
                    self.fields['gender'].initial = self.instance.user.gender



class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs=
    {'placeholder': 'Enter your email address',
     'class': 'form-control',
     'required': True}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("If a user with that emails exits in the system , an email has been sent.Please check your inbox.")
        return email
    

class HealthDataReviewForm(forms.ModelForm):
    class Meta:
        model = PatientHealthData
        fields = ['review_comment', 'review_status']
        widgets = {
            'review_comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter review comments...'
            }),
            'review_status': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
            'required': True
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
            'required': True
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password and self.user:
            try:
                validate_password(password, self.user)
            except ValidationError as error:
                raise forms.ValidationError(error)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        
        return cleaned_data

    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.password = make_password(password)
        self.user.save()
        return self.user






#doctor profile form
class DoctorProfileForm(forms.ModelForm):
    # Define specialty choices for better UX
    SPECIALTY_CHOICES = [
        ('', 'Select your specialty'),
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Emergency Medicine', 'Emergency Medicine'),
        ('Family Medicine', 'Family Medicine'),
        ('General surgery', 'General Surgery'),
        ('Internal Medicine', 'Internal Medicine'),
        ('Neurology', 'Neurology'),
        ('Obstetrics gynecology', 'Obstetrics & Gynecology'),
        ('Oncology', 'Oncology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('Psychiatry', 'Psychiatry'),
        ('Radiology', 'Radiology'),
        ('Other', 'Other'),
    ]
    
    first_name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        }),
        error_messages={
            'required': 'First name is required.'
        }
    )
    
    last_name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        }),
        error_messages={
            'required': 'Last name is required.'
        }
    )
    
    specialty = forms.ChoiceField(
        choices=SPECIALTY_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Please select your medical specialty.'
        }
    )
    
    registration_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your medical registration ID'
        }),
        error_messages={
            'required': 'Medical registration ID is required.'
        }
    )
    
    year_of_birth = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your birth year (e.g., 1985)',
            'min': '1940',
            'max': str(datetime.now().year - 18)
        }),
        error_messages={
            'required': 'Year of birth is required.'
        }
    )
    
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialty', 'registration_id', 'year_of_birth']
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            # Remove extra spaces and capitalize properly
            first_name = first_name.strip().title()
            if not first_name.isalpha():
                raise ValidationError('First name should only contain letters.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            # Remove extra spaces and capitalize properly
            last_name = last_name.strip().title()
            if not last_name.isalpha():
                raise ValidationError('Last name should only contain letters.')
        return last_name
    
    def clean_registration_id(self):
        registration_id = self.cleaned_data.get('registration_id')
        if registration_id:
            registration_id = registration_id.strip().upper()
            # Check if registration_id already exists (excluding current instance if editing)
            existing = Doctor.objects.filter(registration_id=registration_id)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('This registration ID is already in use.')
        return registration_id
    
    def clean_year_of_birth(self):
        year_of_birth = self.cleaned_data.get('year_of_birth')
        if year_of_birth:
            current_year = datetime.now().year
            if year_of_birth < 1940:
                raise ValidationError('Please enter a valid birth year.')
            if year_of_birth > current_year - 18:
                raise ValidationError('You must be at least 18 years old.')
        return year_of_birth
    
    def clean_specialty(self):
        specialty = self.cleaned_data.get('specialty')
        if specialty == '':
            raise ValidationError('Please select your medical specialty.')
        return specialty