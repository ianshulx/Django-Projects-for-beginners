from django.contrib import admin
from banking.models import UserExtension
from banking.models import Transactions

# Register your models here.


admin.site.register(UserExtension)
admin.site.register(Transactions)