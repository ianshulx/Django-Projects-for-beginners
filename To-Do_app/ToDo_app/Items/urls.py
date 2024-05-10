from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addItems", views.addItems, name="addItems"),
    path("deleteItems", views.deleteItems, name="deleteItems"),
    path("updateItems", views.updateItems, name="updateItems"),
    path("statusItems", views.statusItems, name="statusItems"),
]
