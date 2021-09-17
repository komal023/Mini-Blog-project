from django.db import models
from django.contrib.auth.models import User
from .helpers import generate_slug

# Create your models here.
class Blog(models.Model):
    
    Blog_title = models.CharField(null=True,blank=True,max_length=50)
    blog_desc = models.TextField(null=True,blank=True)
    short_content = models.TextField(null=True,blank=True)
    blog_image = models.ImageField(upload_to='static/images/')
    created_at = models.DateTimeField(auto_now=True)
    upload_to = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, blank=True , null=True , on_delete=models.CASCADE)
    slug = models.SlugField(max_length=1000 , null=True , blank=True)

    def __str__(self):
        if self.Blog_title:
            return self.Blog_title
        else:
            return "No title"
    
    def save(self , *args, **kwargs): 
        self.slug = generate_slug(self.Blog_title)
        super(Blog, self).save(*args, **kwargs)
    