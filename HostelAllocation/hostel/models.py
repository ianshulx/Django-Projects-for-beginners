from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=10, choices=[('open', 'Open'), ('reserved', 'Reserved')])
    cet_marks = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Allocation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    allocated_seat = models.BooleanField(default=False)
    allocated_date = models.DateField(auto_now_add=True)
