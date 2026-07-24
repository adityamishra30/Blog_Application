from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATUS_CHOICES=[
    ("draft","Draft"),
    ("published","Published")
]
class Blog(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    cover_image=models.ImageField(upload_to='blog_images/', blank=True, null=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="draft")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
        