import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        messages.get_messages(request)
        return render(request, "authentication/register.html")

    def post(self, request):

        # get user data
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        context = {"fieldValues": request.POST}

        # validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, "Password should be 8 charecter long")
                    return render(request, "authentication/register.html", context)
                else:
                    # new nuser creation process
                    try:
                        # adding user to data base
                        user = User.objects.create_user(username=username, email=email)
                        user.set_password(password)
                        user.save()
                        transaction.commit()
                        messages.success(request, "Account created")
                    except Exception as e:
                        messages.error(request, f"Server - Database warning {str(e)}")
                        transaction.rollback()
            else:
                messages.error(request, "Email already exists")
                return render(request, "authentication/register.html", context)
        else:
            messages.error(request, "User name already exists")
            return render(request, "authentication/register.html", context)

        return redirect("login")


class UserLoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Logged in successfully.")
                    return redirect("index")  # Redirect to the expenses page
                else:
                    messages.error(request, "Your account is not active.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please provide both username and password.")

        return redirect("login")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successfully.")
        return redirect("login")
