from __future__ import unicode_literals
from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    bio = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    notes = models.TextField()
    image = models.ImageField(upload_to='media',blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class Timecard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    hours = models.IntegerField(null=True, blank=True)
    project = models.CharField(max_length=140)
    department = models.CharField(max_length=140)
    funded = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('accounts:timecards')

    def __int__(self):
        return self.created

class TimecardSummary(Timecard):
    class Meta:
        proxy = True
        verbose_name = 'timecard summary'
        verbose_name_plural = 'timecard summaries'
