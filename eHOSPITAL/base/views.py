from django.shortcuts import render,redirect
from django.views.generic import TemplateView

from django.contrib.auth import logout
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class HomePageView(TemplateView):
    template_name = 'base/home.html'


class AboutPageView(TemplateView):
    template_name = 'base/about.html'



class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

class CustomLoginView(LoginView):
    template_name = 'base/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_role == 'patient':
            return reverse_lazy('registration:patient-dashboard', kwargs={'pk': self.request.user.patient.pk}) 
        elif user.user_role == 'doctor':
            return reverse_lazy('registration:doctor-dashboard') 


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

