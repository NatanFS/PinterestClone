from django.db import models
from django.contrib.auth.models import User

class Pin(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='pins/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='pins', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_pins', blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
