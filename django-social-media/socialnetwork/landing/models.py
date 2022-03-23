from distutils.command.upload import upload
from tokenize import blank_re
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):

    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_photos', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    


# Create your models here.
