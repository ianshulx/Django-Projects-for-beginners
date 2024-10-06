from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def IndexView(request):
    return render(request, "events/index.html")


@login_required(login_url="/login")
def DashView(request):
    return render(request, "events/dashboard.html")


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('dash')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")

            return redirect('index')
        else:
            messages.error(
                request, "There was an error logging in. Please try again.")
            return redirect('login')
    return render(request, "events/login.html")


def RegisterView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat-password"]
        print(email, username, password, repeat_password)
        if password != repeat_password:
            messages.error(request, "Passwords do not match")
        try:
            user = User.objects.create_user(
                email=email, username=username, password=password)
            user.save()
            return redirect("login")
        except Exception as e:
            messages.error(request, str(e))
    return render(request, "events/register.html")


@login_required(login_url="/login")
def LogoutView(request):
    logout(request)
    return redirect("index")


@login_required(login_url="/login")
def ProfileView(request):
    return render(request, "events/profile.html")
