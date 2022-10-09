from django import forms
from django.contrib.auth.forms import UserCreationForm

from.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class EditProfileForm(forms.Form):
    username = forms.CharField()
    about_me = forms.CharField(widget=forms.Textarea())
    image = forms.ImageField(required=False)

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def clean_username(self):
        """
        This function throws an exception if the username has already been 
        taken by another user
        """

        username = self.cleaned_data['username']
        if username != self.original_username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    'A user with that username already exists.')
        return username
