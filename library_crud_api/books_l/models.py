from django.db import models

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    rating = models.FloatField()
    cover = models.ImageField(upload_to='book_covers/')

    def __str__(self):
        return self.name
