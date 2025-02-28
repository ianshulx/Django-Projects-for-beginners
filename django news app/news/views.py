from django.shortcuts import render
from django.http import JsonResponse
import json
import requests

def home(request):  
    #for news search
    if request.method == "POST":
        search_query = request.POST.get("search_term") 
        news_api_request=requests.get(f"https://newsapi.org/v2/everything?q={search_query}&apiKey=535b8edca7c54c5f9d01f5496d3b7a08")
    else:
        news_api_request=requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=535b8edca7c54c5f9d01f5496d3b7a08")
    api=json.loads(news_api_request.content)
    return render(request,'index.html',{'api':api})

# def searchnews(request):
#     news_api_request=requests.get(f"https://newsapi.org/v2/top-headlines?q={request.POST.get()}&apiKey=(apikey)")
#     api=json.loads(news_api_request.content)
#     return render(request,'index.html',{'api':api})

