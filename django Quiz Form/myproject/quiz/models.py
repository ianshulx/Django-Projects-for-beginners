from django.db import models
class QuizResult(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    date = models.DateTimeField(auto_now_add=True)