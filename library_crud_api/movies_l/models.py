from django.db import models

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    cover = models.ImageField(upload_to='movie_covers/')

    def __str__(self):
        return self.name
