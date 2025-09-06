from django.db import models
from datetime import date
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Post(models.Model):
    post_header = models.CharField(max_length=30)
    post_text = models.TextField()
    post_date = models.DateField(default=date.today)
    post_time = models.TimeField(auto_now_add=True, editable=False)
    image = CloudinaryField('image', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_like_count(self):
        return self.likes.count()

    def __str__(self):
        return self.post_header