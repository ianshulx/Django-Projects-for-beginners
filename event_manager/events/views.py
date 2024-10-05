from django.shortcuts import render
from django.views import generic


def IndexView(request):
    return render(request, "events/index.html")


def LoginView(request):
    return render(request, "events/login.html")