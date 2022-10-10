from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #Additional Fields
    current_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Transactions(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdraw_transactions')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_transactions')
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)




