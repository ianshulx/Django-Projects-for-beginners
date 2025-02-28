from django.shortcuts import render
from django.http import JsonResponse
import json
import requests

def home(request):  
    #for news search
    if request.method == "POST":
        search_query = request.POST.get("search_term") 
        news_api_request=requests.get(f"https://newsapi.org/v2/everything?q={search_query}&apiKey=(your_api_key)")
    else:
        news_api_request=requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=(your_api_key)")
    api=json.loads(news_api_request.content)
    return render(request,'index.html',{'api':api})

# def searchnews(request):
#     news_api_request=requests.get(f"https://newsapi.org/v2/top-headlines?q={request.POST.get()}&apiKey=(apikey)")
#     api=json.loads(news_api_request.content)
#     return render(request,'index.html',{'api':api})

