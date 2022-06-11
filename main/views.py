from email import message
import re
import django.contrib.messages as messages
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.db import transaction
from requests import post
from .forms import *


class HomeView(View):
    """
    View representing the home page
    """
    template_name = 'home/home.html'

    def get(self, request: HttpRequest):
        current_user = request.user
        posts = Post.objects.filter(user__username=current_user.username)

        return render(request, self.template_name, {
            'posts': posts,
            'title': 'Home',
            'current_user': current_user
        })


class LoginView(View):
    """
    View presenting the login page
    """
    template_name = 'home/login.html'

    def get(self, request: HttpRequest):
        current_user = request.user
        return render(request, self.template_name, {
            'title': 'Login',
            'current_user': current_user
        })


class LogoutView(View):
    """
    View handling logout request
    """

    def get(self, request):
        auth_logout(request)
        return redirect('app:login')


class PostCreateEditView(View):
    """
    View handling post creation and edit
    """
    template_name = 'post/post_create_edit.html'

    def get(self, request: HttpRequest):
        current_user = request.user

        form = PostForm()
        return render(request, self.template_name, {
            'action': 'Create new',
            'form': form,
            'title': 'New post',
            'current_user': current_user
        })

    def post(self, request: HttpRequest):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                post_obj = form.save(commit=False)
                post_obj.user = request.user
                post_obj.save()
            messages.success(request, 'Successfully added a new post')
            return redirect('app:home')
        else:
            form_errors = form.errors.get_json_data()
            for field in form_errors:
                msgs = form_errors[field]
                for msg in msgs:
                    render_msg = msg['message']
                    messages.error(request, f'Error in field {field}: {render_msg}')
            return redirect('app:post_create_edit')
