from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User



# For Income Categories
class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='user_inc_catg', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
# For Expense Categories
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='user_exp_catg', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, related_name='user_name', on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    date = models.DateField(default=date.today())
    amount= models.FloatField()
    category = models.ForeignKey(IncomeCategory, related_name='income_catg', on_delete=models.CASCADE)
    note=models.TextField()

    def __str__(self):
        return f"Income of Rs.{self.amount} for {self.name}"


class Expense(models.Model):
    user =models.ForeignKey(User,  related_name='Exp_user_name', on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    date = models.DateField(default=date.today())
    amount= models.FloatField()
    category = models.ForeignKey(ExpenseCategory, related_name='expense_catg', on_delete=models.CASCADE)
    note=models.TextField()

    def __str__(self):
        return f"Rs.{self.amount} spent for {self.name}"
    
class Budget(models.Model):
    user =models.ForeignKey(User,  related_name='budget_user', on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    balance = models.FloatField(default=0)
    details= models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Account(models.Model):
    user=models.ForeignKey(User,  related_name='user_Ac', on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    balance = models.FloatField(default=0)
    details= models.CharField(max_length=100)

    def __str__(self):
        return self.name


