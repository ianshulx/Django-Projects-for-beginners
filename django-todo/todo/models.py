from django.db import models

class Item(models.Model):
    content = models.TextField()
