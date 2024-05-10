from django.urls import path
from .views import (
    RegistrationView,
    UserLoginView,
    UserLogoutView,
)

urlpatterns = [
    # django always checks for cross site forgery so we add csrf_exempt to let other sites send reuest to this url
    path("registration", RegistrationView.as_view(), name="registration"),
    path("userlogin", UserLoginView.as_view(), name="login"),
    path("userlogout", UserLogoutView.as_view(), name="logout"),
]
