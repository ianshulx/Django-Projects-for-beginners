from django.shortcuts import render

# Create your views here.
def musichomeaction(request):
   
    return render(request, 'music_homepage.html')