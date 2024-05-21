from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Pin(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='pins/', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='pins', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_pins', blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        max_size = (800, 800)

        if img.height > max_size[0] or img.width > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(self.image.path)
