

import uuid
from django.db import models
from course.models import *
from django.contrib.auth.models import User

from user_profile.models import slug_generator
# Create your models here.
class product_detail(models.Model):
    product_img=models.ImageField(upload_to='image/shop/')
    product_title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,max_length=1000)
    product_price=models.IntegerField()
    about_product=models.TextField()
    product_description=models.TextField()
    product_tag=models.CharField(max_length=100)
    quntity=models.IntegerField()
    product_sku=models.IntegerField()
    category=models.CharField(max_length=100)
    created_date=models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slug_generator(product_detail,self.product_title)
        super(product_detail, self).save(*args, **kwargs)
  
    def __str__(self):
        return self.product_title

class shop_review(models.Model):
    shop=models.ForeignKey(product_detail,on_delete=models.CASCADE)
    review=models.TextField()
    rate=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.shop.product_title[:20] +' - '+self.review[:20]
 

class coupon_code(models.Model):
    code=models.IntegerField()
    valid_date=models.DateField()
    discount=models.IntegerField(null=True)
class cart(models.Model):
    userid=models.IntegerField()
    slug=models.SlugField(null=True)
    prod_id=models.IntegerField()
    prod_name=models.CharField(max_length=100)
    quntity=models.IntegerField()
    coupon=models.IntegerField(default=0)



class product_order(models.Model):
    product=models.ForeignKey(product_detail,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    uid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    company=models.CharField(max_length=100,blank=True)
    country=models.CharField(max_length=50)
    address=models.TextField()
    city=models.CharField(max_length=50)
    province=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    phone=models.IntegerField()
    email=models.EmailField()
    quntity=models.IntegerField()
    payment=models.CharField(max_length=100)
    amount=models.IntegerField()
    order_notes=models.TextField(blank=True)
    order_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.product_title[:10]+' '+self.fname+self.lname
 



class course_order(models.Model):
    course=models.ForeignKey(course_detail,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    uid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    company=models.CharField(max_length=100,blank=True)
    country=models.CharField(max_length=50)
    address=models.TextField()
    city=models.CharField(max_length=50)
    province=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    phone=models.IntegerField()
    email=models.EmailField()
    quntity=models.IntegerField()
    payment=models.CharField(max_length=100)
    amount=models.IntegerField()
    order_notes=models.TextField(blank=True)
    order_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.course.course_title[:10]+' '+self.fname+self.lname
 





class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."