from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)


# Database trigger when a new user is created
@receiver(post_save, sender=User)
def create_profile_signal(sender, instance, created, **kwargs):
    # If a new user is created: create a new profile for it
    if created:
        Profile.objects.create(user=instance)
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Post(models.Model):
    user = models.ForeignKey(verbose_name='Username',
                             to=User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Post title', max_length=100)
    content = models.TextField(verbose_name='Post content')
    date_created = models.DateField(verbose_name='Date created', auto_now_add=True)
