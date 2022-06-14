from django import forms
from django.forms import widgets
from .models import *


class PostForm(forms.ModelForm):
    """
    Form for creating and editing a post
    """

    class Meta:
        model = Post
        exclude = ["user", "date_created"]
