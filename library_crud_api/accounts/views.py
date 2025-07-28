from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.


def register_view(request):
    """ 
    This view renders the signup page and handles the signup action.
    
    If the request method is GET, it renders the signup page with the UserCreationForm.
    
    If the request method is POST, it checks if the passwords match. If they do, it creates a new user with the given username and password, saves it, logs the user in and redirects to the home page. If the passwords don't match, it renders the signup page with the UserCreationForm and an error message. If the username already exists, it renders the signup page with the UserCreationForm and an error message.
    """
    if request.method == 'GET':
        return render(request, 'register/signup.html', {
            'form': UserCreationForm
        })

    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'register/signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })

        return render(request, 'register/signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })


def login_view(request):
    """
    This view renders the login page and handles the login action.
    
    If the request method is GET, it renders the login page with the AuthenticationForm.
    
    If the request method is POST, it authenticates the user. If the authentication is successful, it logs the user in and redirects to the home page. If the authentication fails, it renders the login page with the AuthenticationForm and an error message.
    """
    if request.method == 'GET':
        return render(request, 'register/login.html', {
            'form': AuthenticationForm
        })

    elif request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'register/login.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })

        login(request, user)
        return redirect('home')


@login_required
def logout_view(request):
    """
    This view logs the user out and redirects to the home page.

    :param request: The HTTP request object
    :return: An HTTP response object
    """
    logout(request)
    return redirect('home')


def home(request):
    """
    This view renders the home page.
    
    If the request method is GET, it renders the home.html template.
    """
    return render(request, 'home.html')


def about(request):
    """
    This view renders the about page.
    
    If the request method is GET, it renders the about.html template.
    """
    return render(request, 'about.html')
