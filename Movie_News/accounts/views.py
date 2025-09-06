from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def loginview(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("blog:index")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    return render(request, "login.html")

def signupview(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password")
        confirm_password = request.POST["confirm_password"]

        if not username or not password or not confirm_password:
            return render(request, "signup.html", {
                "error_message": "All fields are required."
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error_message": "User  already exists"
            })


        if password == confirm_password:
            user = User.objects.create_user(username = username, password = password)
            user.save()
            login(request, user)
            return redirect("blog:index")
        else:
            error_message = "Passwords do not match!"
            return render(request, "signup.html", {"error_message": error_message})

    return render(request, "signup.html")


def logoutview(request):
    logout(request)
    return redirect("blog:index")