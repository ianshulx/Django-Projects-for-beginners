import uuid
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

reqd_user=get_user_model()

class Profile(models.Model):
    user=models.ForeignKey(reqd_user,on_delete=models.CASCADE)
    bio=models.CharField(max_length=10000,default='Busy')
    profile_img=models.ImageField(upload_to='media',default='image.jpeg')
    location=models.CharField(max_length=1000,blank=True)
    followers=models.IntegerField(default=0)
    following=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    post_id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    Profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    Img=models.ImageField(upload_to='post_images')
    caption=models.CharField(max_length=10000)
    time=models.DateTimeField(default=datetime.now)
    likes=models.IntegerField(default=0)

    def is_liked_by(self,user):
        return Liked_Post.objects.filter(Username=user.username,post_id=self.post_id).exists()
          
    def __str__(self):
        return self.Profile.user.username 
    
class Liked_Post(models.Model):
    Username=models.CharField(max_length=100)
    post_id=models.UUIDField()
    def __str__(self):
        return self.Username
    
class Comment(models.Model):
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    content=models.CharField(max_length=1000)
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Follow(models.Model):
    current_user=models.ForeignKey(reqd_user,on_delete=models.CASCADE)
    followed=models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.current_user.username+"followed"+self.followed.user.username