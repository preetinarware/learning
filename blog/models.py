
import imp
from django.db import models
from user_profile.models import*
from blog.models import*
# Create your models here.

class blogdetail_img(models.Model):
    # blogs=models.ForeignKey(blog_detail,on_delete=models.CASCADE)
    imgs=models.ImageField(upload_to='image/blog/')
    def __str__(self) -> str:
        return str(self.imgs)[:20]
from user_profile.models import slug_generator

class blogdetail_element(models.Model):
    # blogs=models.ForeignKey(blog_detail,on_delete=models.CASCADE)
    element=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.element[:60]

class blog_detail(models.Model):
    blog_instructor=models.ForeignKey(instructor,on_delete=models.CASCADE,related_name='blog_detail')
    blog_category=models.CharField(max_length=100)
    blog_title=models.CharField(max_length=500)
    slug=models.SlugField(max_length=1000,unique=True) 
    blog_img=models.ImageField(upload_to='image/blog/')
    blog_description=models.TextField()
    blog_created_date=models.DateField(auto_now=True)
    tags=models.CharField(max_length=100)
    #for full blog detail
    head1=models.TextField()
    head2=models.TextField()
    imgs=models.ManyToManyField(blogdetail_img,related_name='blog_img')
    element=models.ManyToManyField(blogdetail_element,related_name='blog_element')
    setting=models.TextField()
    why_need=models.TextField()
    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slug_generator(blog_detail,self.blog_title)
        super(blog_detail, self).save(*args, **kwargs)
  
    def __str__(self):
        return self.blog_title


class review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog_id=models.ForeignKey(blog_detail,on_delete=models.CASCADE)
    comment=models.TextField()

    def __str__(self):
        return self.user.username+' '+self.blog_id.blog_title