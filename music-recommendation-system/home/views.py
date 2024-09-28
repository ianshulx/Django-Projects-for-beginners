from django.shortcuts import render,HttpResponse
import pandas as pd
from pycode.music_rec import recommend,list_music
from home.forms import inputform


# Create your views here.
def home(request):
    return render(request, 'index.html')
def index(request):
    return render(request, "index.html")

def music_list(request):
    list_1=list_music()
    l=list_1
    return render(request,'index.html',{'l':l})
def recommend_music(request):
    if request.method=='POST':
        fav_music=str(request.POST.get('fav_music'))
        recommendations = recommend(fav_music)
        rec=recommendations
        return render(request,'index.html',{'rec':rec})
    return render(request,'index.html')