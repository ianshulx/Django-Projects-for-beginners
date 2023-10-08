from django.contrib import admin
from .models import IncomeCategory,ExpenseCategory,Income,Expense,Account

# Register your models here.
admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)

# TO Modify INcome page for admin
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['user','name','date','amount','category','note']
    search_fields = ('user','name', 'category')
    list_filter = ('user','category','date')
admin.site.register(Income, IncomeAdmin)

# TO Modify Expenses page for admin
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user','name','date','amount','category','note']
    search_fields = ('user','name', 'category')
    list_filter = ('user','category','date')
admin.site.register(Expense, ExpenseAdmin)

# TO Modify Account page for admin
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user','name','balance']
admin.site.register(Account, AccountAdmin)