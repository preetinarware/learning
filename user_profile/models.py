
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class instructor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user")
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=1000,unique=True)
    email=models.EmailField()
    img=models.ImageField(blank=True,upload_to='image/user_profile/')
    expert=models.TextField()
    about=models.TextField()
    facebook=models.URLField(max_length=200,null=True)
    twitter=models.URLField(max_length=200,null=True)
    youtube=models.URLField(max_length=200,null=True)
    linkedin=models.URLField(max_length=200,null=True)
   
    def __str__(self):
        return self.name




class student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=1000,unique=True)
    email=models.EmailField()
    img=models.ImageField(blank=True,upload_to='image/user_profile/')
    about=models.TextField(null=True)
    facebook=models.URLField(max_length=200,null=True)
    twitter=models.URLField(max_length=200,null=True)
    youtube=models.URLField(max_length=200,null=True)
    linkedin=models.URLField(max_length=200,null=True)
   
   
    def __str__(self):
        return self.name