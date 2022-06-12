import traceback
import facebook
import logging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField
from social_django.models import UserSocialAuth


logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar_link = models.TextField(null=True)

    @property
    def avatar_url(self):
        if self.avatar_link:
            return self.avatar_link
        else:
            return ''

    @staticmethod
    def update_avatar_url(user):
        try:
            # Get user access token from server database
            auth = UserSocialAuth.objects.get(user_id=user.id)
            auth_extra_data = auth.extra_data
            access_token = auth_extra_data['access_token']
            fb_user_id = auth_extra_data['id']
            logger.info('Facebook user ID acquired')

            # Intialize facebook graph API
            graph = facebook.GraphAPI(access_token=access_token)
            # Get avatar information
            avatar_data = graph.get_object(id=fb_user_id, fields='picture')
            avatar_link = avatar_data['picture']['data']['url']
            logger.info('Avatar link acquired')

            # Save avatar information to server database
            profile = Profile.objects.get(user=user)
            profile.avatar_link = avatar_link
            profile.save()
        except Exception as e:
            logger.error('Cannot fetch profile picture link for user: %d', user.id)
            logger.error(traceback.format_exc())


# Database trigger when a new user is created
@receiver(post_save, sender=User)
def create_profile_signal(sender, instance, created, **kwargs):
    # If a new user is created: create a new profile for it
    if created:
        Profile.objects.create(user=instance)

    if hasattr(instance, 'profile'):
        instance.profile.save()


# When user logs in: update profile image path
@receiver(user_logged_in)
def login_update_profile_pic(sender, request, user, **kwargs):
    Profile.update_avatar_url(user)


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


# Database trigger when a post is deleted: delete corresponding blob on S3
@receiver(post_delete, sender=Post)
def auto_delete_s3_post(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)



# Updates the user profile picture after user authentication
def profile_picture_update_handler(strategy, user, response, details,
                         is_new=False,*args,**kwargs):
    logger.info('End of authentication process')
    logger.info(f'User id: {user}')
    Profile.update_avatar_url(user)