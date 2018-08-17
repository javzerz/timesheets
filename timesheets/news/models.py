from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class News_Article(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    body = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title
