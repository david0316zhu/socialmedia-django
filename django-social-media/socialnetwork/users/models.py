from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from PIL import Image



# Create your models here\

class ProfileManager(models.Manager):
    

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    objects = ProfileManager()


    def __str__(self):
        return f'{self.user.username} Profile'

    def get_friends(self):
        return self.friends.all()

    def get_num_friends(self):
        return self.friends.all().count()


    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)

    
STATUS_CHOICES = (('send', 'send'), ('accepted', 'accepted'))


class RelationshipManager(models.Manager):
    def request_received(self, receiver):
        query = Relationship.objects.filter(receiver=receiver, status='send')
        return query

    

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now=True)
    objects = RelationshipManager()
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"