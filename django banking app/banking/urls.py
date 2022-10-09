from django.urls import path
from banking import views

app_name = 'banking'

urlpatterns = [
    path('',views.index,name="index"),
    path('customers',views.customers,name="customers"),
    path('customers/search',views.customers_search,name="customers_search"),
    path('customers/transact/<int:pk>',views.transaction,name="transact"),
    path('customers/transact/<int:pk>/search',views.transact_customers_search,name="transact_customers_search"),
    path('records',views.RecordsView.as_view(),name="records"),
]