#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
import markdown

# Create your models here.

class Article(models.Model):
    author = models.CharField(max_length=100)
    url = models.URLField()
    title = models.CharField(max_length=100)
    title_zh = models.CharField(max_length=100)
    content_md = models.TextField()
    content_html = models.TextField()
    tags = models.CharField(max_length=30)
    views = models.IntegerField(default=0)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    
    class Meta():
        ordering = ['-created', '-updated']
        
    def __unicode__(self):
        return self.title