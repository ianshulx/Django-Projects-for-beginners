from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request,'home/index.html')


class EnglishView(View):
    def get(self, request):
        return render(request,'home/indexEn.html')

