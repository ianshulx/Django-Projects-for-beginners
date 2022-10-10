from django.db import models


# Create your models here.
class Mail(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=252, blank=False)
    words = models.TextField(max_length=5000, blank=True, null=True)


    def __str__(self):
        return self.url
