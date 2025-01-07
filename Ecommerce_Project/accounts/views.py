import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def RegisterUser(request):
    if request.method == 'POST' and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        username_pattern = r'^[a-zA-Z0-9_]{3,30}$'

        if not firstname or not lastname or not username or not email or not password:
            return JsonResponse({'success': False, 'error': "All fields are required!"}, status=400)
        
        if not re.match(username_pattern, username):
            return JsonResponse({'success': False, 'error': 'Username must be 3-30 characters long and can only contain letters, digits, and underscores!'}, status=400)
        
        if User.objects.filter(username = username).exists():
            return JsonResponse({'success': False, 'error': "Username already exists!"}, status=400)
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'success': False, 'error': "Email Address is already registered!"}, status=400)
        
        if len(password) < 6:
            return JsonResponse({'success': False, 'error': "Password must be at least 6 characters long"}, status=400)
        
        user = User.objects.create_user(
            first_name = firstname,
            last_name = lastname,
            username = username,
            email = email,
            password = password
        )
        user.save()
        
        return JsonResponse({'success': True, 'message': "Account created successfully"}, status=200)

    return JsonResponse({'success': False, 'error': "Invalid Request"}, status=400)