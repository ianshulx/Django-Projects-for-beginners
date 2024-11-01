import paypalrestsdk
from django.shortcuts import render, redirect, get_object_or_404
from .models import Courses
from django.conf import settings
from django.http import JsonResponse

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET_KEY,
})

def courses_list(request):

    courses = Courses.objects.all()

    return render(request, 'course_list.html', {"courses": courses})

def course_detail(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    return render(request, 'course_detail.html', {'course': course, 'CLIENT_ID': settings.PAYPAL_CLIENT_ID})

def create_order(request, course_id):
    """View to handle PayPal order creation"""
    course = get_object_or_404(Courses, id=course_id)
    
    # Create the PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(f'/courses/{course_id}/payment-success'),
            "cancel_url": request.build_absolute_uri(f'/courses/{course_id}/payment-cancel')
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": course.title,
                    "sku": course.id,
                    "price": str(course.price),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(course.price),
                "currency": "USD"
            },
            "description": f"Purchase of {course.title}."
        }]
    })
    
    if payment.create():
        # Redirect user to PayPal for payment approval
        for link in payment.links:
            if link.rel == "approval_url":
                return JsonResponse({'approval_url': link.href})  # Return the approval URL as JSON
    else:
        # Handle payment creation failure
        return JsonResponse({'error': payment.error}, status=400)

def payment_success(request, course_id):
    """View to handle successful PayPal payments"""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        # Payment was successful
        return render(request, 'payment_success.html', {'payment': payment})
    else:
        # Handle payment execution failure
        return JsonResponse({'error': payment.error}, status=400)

def payment_cancel(request, course_id):
    """View to handle payment cancellation"""
    return render(request, 'payment_cancel.html')
