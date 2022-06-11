import boto3
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar')


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
    image = models.ImageField(verbose_name='Image', upload_to='post_images', null=True)
    place_name = models.CharField(verbose_name='Place name', max_length=255, default='')
    location = PlainLocationField(
        based_fields=['place_name'], default='10.762622,106.660172')
    date_created = models.DateField(
        verbose_name='Date created', auto_now_add=True)


@receiver(post_delete)
def auto_delete_s3_post(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
