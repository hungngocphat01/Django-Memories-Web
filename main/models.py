import boto3
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar_url = models.TextField(null=True)


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
    image = models.ImageField(verbose_name='Image',
                              upload_to='post_images', null=True, blank=True, help_text='If you do not provide an image, a random image will be shown when displaying this post.')
    place_name = models.CharField(verbose_name='Place name', max_length=255,
                                  default='', help_text='Enter some text here, and the map below will change')
    location = PlainLocationField(
        based_fields=['place_name'], default='10.762622,106.660172', help_text='You can zoom, click on the map to  select a location')
    date_created = models.DateField(
        verbose_name='Date created', auto_now_add=True)

    @property
    def img_url(self):
        # Returns random image if this post is not attached with any
        if self.image:
            return self.image.url
        return 'https://picsum.photos/1000/500'


@receiver(post_delete, sender=Post)
def auto_delete_s3_post(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
