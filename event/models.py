from django.db import models

# Create your models here.




class event_detail(models.Model):
    
    event_img=models.ImageField(upload_to='image/event/')
    event_title=models.CharField(max_length=1000) 
    slug=models.SlugField(max_length=1000,unique=True) 
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    date=models.DateField()
    event_cost=models.IntegerField()
    event_total_slot=models.IntegerField(default=0)
    event_booked_slot=models.IntegerField(default=0)
    event_start_date=models.DateField()
    event_end_date=models.DateField()
    event_start_time=models.TimeField()
    event_end_time=models.TimeField()
    about_event=models.TextField()
    where_event=models.TextField()


    def __str__(self):
        return self.event_title
