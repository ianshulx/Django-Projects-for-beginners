from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Items(models.Model):
    date = models.DateField(null=True)
    description = models.TextField(null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    category = models.CharField(max_length=100)

    def get_formatted_date(self):
        return self.date.strftime("%Y-%m-%d") if self.date else None

    def __str__(self):
        return (str(self.owner) +" " + str(self.source))

    class Meta:
        ordering = ["-date"]


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
