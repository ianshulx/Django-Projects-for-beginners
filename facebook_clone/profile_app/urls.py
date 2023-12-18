from django.urls import path
from .views import profile_index, edit_profile, edit_profile_image

urlpatterns = [
    path('', profile_index, name="profile-index"),
    path('edit-profile/', edit_profile, name="edit-profile"),
    path('edit-profile-image/', edit_profile_image, name='edit-profile-image')
]
