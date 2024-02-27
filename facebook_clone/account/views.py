from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from .models import Accounts
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# import threading
# import validate_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.



# User Register View


def register_view(request):
    if request.user.is_authenticated:
        print("Your are already Logged In")
    context = {}

    if request.POST:

        form = RegisterForm(request.POST or None)

        if form.is_valid():
            user_form = form.save()
            # print(user_form)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            # print(user)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("index")
                else:
                    print("User not active")
            else:
                print("Invalid User")
        else:
            print(form.errors.as_data())
            context["reg_form"] = form
    else:
        print("Http request not valid")
    return render(request, 'account/register.html', context)


# User Login View
def login_view(request):
    context = {}
    if request.method == "POST":
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    destination = get_redirect_if_exist(request)
                    if destination:
                        return redirect(destination)
                    return redirect("index")
        context["login_form"] = login_form

    return render(request, 'account/login.html', context)


def get_redirect_if_exist(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get('next'))
    return redirect


# User logout View
@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')


# User Reset Password Form.
'''
Here Pasword reset Link is being sent to a regestered email
'''


def forgot_password(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get('email')
        # print(email)

        context = {
            'values': request.POST
        }

        current_site = get_current_site(request)
        user = Accounts.objects.filter(email=email)
        if user.exists():
            email_content = {
                'user': user[0],
                'doamin': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }

            link = reverse('reset-user-pass', kwargs={
                'uidb64': email_content['uid'], 'token': email_content['token']
            })

            reset_url = f'http://{current_site.domain}{link}'

            message = f"Hi {user[0].username}, Kindly click the link below to reset your password\n {reset_url}"
            print(message)

            messages.success(
                request, f"You copy the link in the console")
            redirect('login')
        else:
            messages.success(
                request, "Account not valid, Kindly provide a valid email account")
            redirect('forgot-password')
    return render(request, 'account/forget_password_form.html', context)


# User Reset Password
def resetPass(request, uidb64, token):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        print(password1)
        password2 = request.POST.get('password2')
        (password2)
        if password1 != password2:
            messages.info(request, "Password deos not match")
            return render(request, "account/password_reset_form.html")
        if len(password1) < 6:
            messages.info(request, "Password too short")
            return render(request, "account/password_reset_form.html")

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Accounts.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            if PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password link invalid, Pls request for a new one')
                return redirect('forgot-password')
            messages.info(request, "Password was set successfully")
            return redirect('login')
        except Exception as identifier:
            messages.info(request, 'something went wrong')
            return render(request, "account/reset_password_form.html")
    else:
        print("Enter something")
    return render(request, "account/password_reset_form.html")

