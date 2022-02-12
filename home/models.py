from django.db import models

# Create your models here.


class Newsletter_subscriber(models.Model):
    suscriber_email=models.EmailField()

    def __str__(self):
        return self.suscriber_email