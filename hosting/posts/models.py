from turtle import title
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    content = models.TextField()
    date_create = models.DateTimeField()
