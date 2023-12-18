from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Accounts
from django.contrib.auth import authenticate


"""
Registration Form to sign up users
"""
class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length = 255, help_text = "Required. Add a valid email addrress")
    
    class Meta:
        model = Accounts
        fields = ('email', 'username', 'password1', 'password2',)

    
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            Accounts.objects.get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"This username {username} already in use")
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            Accounts.objects.get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"This username {email} already in use")
    
    def clean(self):
        if self.is_valid():
            password1 = self.cleaned_data["password1"]
            password2 = self.cleaned_data["password2"]
            if password1 != password2:
                raise forms.ValidationError("Password does not match")
    

"""
User Login Form to authenticate user into the system
"""
class LoginForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ('email', 'password',)

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email = email, password = password):
                raise forms.ValidationError(f"Invalid email or password")