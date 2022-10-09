from django.urls import path
from donate import views

app_name = 'donate'

urlpatterns = [
    path('',views.index,name="index"),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]