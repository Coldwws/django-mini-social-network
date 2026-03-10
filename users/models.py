from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.user.username


@receiver
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)