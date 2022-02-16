
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.utils.text import slugify

import random ,string
def get_random_string(size):
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = size))
def slug_generator(instance, new_slug=None):
  
    slug=slugify(new_slug)[:50]
    Klass = instance
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = slugify(str(slug)[:46]+get_random_string(4))
        return slug_generator(instance, new_slug=new_slug)
    return slug


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
    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slug_generator(instructor,self.user.username)
        super(instructor, self).save(*args, **kwargs)
  
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
    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slug_generator(student,self.user.username)
        super(student, self).save(*args, **kwargs)
  
   
    def __str__(self):
        return self.name