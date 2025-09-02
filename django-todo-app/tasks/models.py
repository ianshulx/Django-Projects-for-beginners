from django.conf import settings
from django.db import models

# Create your models here.


# task model
class Task(models.Model):
    PRIORITY_CHOICES = [
        ("L", "Low"),
        ("M", "medium"),
        ("H", "High"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=False)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default="M")
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
