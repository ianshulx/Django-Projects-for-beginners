# courses/models.py

from django.db import models

class Courses(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
