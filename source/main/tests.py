import secrets
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *


class UserProfileTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_username = secrets.token_hex(10)

    def setUp(self):
        u = User.objects.create(username=self.test_username)
        u.save()

    def test_profile_trigger(self):
        # A profile should be created when a user is created
        self.assertTrue(
            Profile.objects.filter(user__username=self.test_username).exists(),
            "Profile was not created",
        )

        # The corresponding profile should be deleted when a user is deleted
        User.objects.get(username=self.test_username).delete()
        self.assertFalse(
            Profile.objects.filter(user__username=self.test_username).exists(),
            "Profile was not deleted",
        )

        # All posts should be deleted as well
        self.assertFalse(
            Post.objects.filter(user__username=self.test_username).exists(),
            "Corresponding posts was not deleted",
        )
