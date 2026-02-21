from django.shortcuts import render
from .models import News

def home(request):
    query = request.GET.get('search', '')  # URL থেকে search term নেওয়া
    if query:
        news_items = News.objects.filter(title__icontains=query)
    else:
        news_items = News.objects.all()

    context = {
        'news_items': news_items,
        'search_query': query,
    }
    return render(request, 'news/news_list.html', context)
