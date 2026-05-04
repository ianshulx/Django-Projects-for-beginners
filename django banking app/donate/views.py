from django.shortcuts import render
import razorpay
from django.conf import settings
import django.views.decorators.csrf
from django.http import HttpResponse, HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 
 
def index(request):
    context = {}
    return render(request, 'banking/donate.html', context=context)


