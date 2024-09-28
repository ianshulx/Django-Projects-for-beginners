from django.shortcuts import render


def signout(request):
   
    return render(request, 'signout.html')