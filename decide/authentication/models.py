from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    sex = models.CharField(max_length=30, blank=False)
    age = models.PositiveIntegerField()
    status = models.CharField(max_length=30, blank=False)
    discord_account = models.CharField(max_length=30, blank=True)
    
    country=CountryField()
    
    def __str__(self):
        return self.user.username



