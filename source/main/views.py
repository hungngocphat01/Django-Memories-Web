import django.contrib.messages as messages
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin as DefaultLoginRequiredMixin
from django.core.exceptions import *
from django.db import transaction
from django.http import Http404, HttpRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import *


class LoginRequiredMixin(DefaultLoginRequiredMixin):
    raise_exception = True
    permission_denied_message = "You do not have access to this content because you are not logged in.\r\nPlease go back to our homepage."


class HomeView(View):
    """
    View representing the home page
    """

    template_name = "home/home.html"

    def get(self, request: HttpRequest):
        try:
            current_user = request.user
            if not current_user.is_authenticated:
                return redirect("app:login")

            posts = Post.objects.filter(user__username=current_user.username)

            return render(
                request,
                self.template_name,
                {"posts": posts, "title": "Home", "current_user": current_user},
            )
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()


class LoginView(View):
    """
    View presenting the login page
    """

    template_name = "home/login.html"

    def get(self, request: HttpRequest):
        try:
            current_user = request.user

            # Don't let the user access the login page if they has logged in
            if current_user.is_authenticated:
                return redirect("app:home")

            return render(
                request,
                self.template_name,
                {"title": "Login", "current_user": current_user},
            )
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()


class LogoutView(LoginRequiredMixin, View):
    """
    View handling logout request
    """

    def get(self, request):
        try:
            auth_logout(request)
            return redirect("app:login")
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()


class BasePostCreateEditView(LoginRequiredMixin, View):
    """
    Base method for creating and editing a post
    """

    template_name = "post/post_create_edit.html"

    def __process_validation_err(self, request, form):
        # Get all errors from form
        form_errors = form.errors.get_json_data()
        # Send error messages to client
        for field in form_errors:
            msgs = form_errors[field]
            for msg in msgs:
                render_msg = msg["message"]
                messages.error(request, f"Error in field {field}: {render_msg}")
        # Redirect to same page
        return redirect("app:post_create")


class PostCreateView(BasePostCreateEditView):
    """
    Handle post creation page
    """

    def get(self, request: HttpRequest):
        try:
            current_user = request.user
            # Create new post for current user
            form = PostForm()
            return render(
                request,
                self.template_name,
                {
                    "action": "Create new",
                    "form": form,
                    "title": "New post",
                    "current_user": current_user,
                },
            )
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()

    def post(self, request: HttpRequest):
        try:
            # Create new form
            form = PostForm(request.POST, request.FILES)
            # Validate and append to DB
            if form.is_valid():
                with transaction.atomic():
                    post_obj = form.save(commit=False)
                    post_obj.user = request.user
                    post_obj.save()
                messages.success(request, "Successfully added a new post")
                return redirect("app:home")
            else:
                raise ValidationError()
        except ValidationError:
            return self.__process_validation_err(request, form)
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()


class PostEditView(BasePostCreateEditView):
    """
    Handle post edit page
    """

    def get(self, request: HttpRequest, post_id):
        try:
            current_user = request.user
            post = Post.objects.get(id=post_id, user__username=current_user.username)

            form = PostForm(instance=post)
            return render(
                request,
                self.template_name,
                {
                    "action": "Edit ",
                    "form": form,
                    "title": "Edit post",
                    "current_user": current_user,
                },
            )
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()

    def post(self, request: HttpRequest, post_id):
        try:
            # Get current user
            current_user = request.user

            # Get corresponding post
            post = Post.objects.get(id=post_id, user__username=current_user.username)

            # Create new form
            form = PostForm(request.POST, request.FILES, instance=post)
            # Validate and append to DB
            if form.is_valid():
                print(request.FILES)
                with transaction.atomic():
                    post_obj = form.save(commit=False)
                    post_obj.user = request.user
                    post_obj.save()
                messages.success(request, "Successfully edit the new post")
                return redirect("app:post_view", post_id)
            else:
                raise ValidationError()
        except ObjectDoesNotExist:
            raise Http404()
        except ValidationError:
            return self.__process_validation_err(request, form)
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()


class PostView(LoginRequiredMixin, View):
    """
    View presenting content of a post
    """

    template_name = "post/view_post.html"

    def get(self, request: HttpRequest, post_id):
        try:
            # Get requested post
            current_user = request.user
            post = Post.objects.get(id=post_id, user__username=current_user.username)

            # Render to client
            return render(
                request,
                self.template_name,
                {"title": post.title, "current_user": current_user, "post": post},
            )
        except ObjectDoesNotExist:
            raise Http404()
        except Exception as e:
            raise


class PostDelete(LoginRequiredMixin, View):
    """
    View handling post deletion
    """

    def get(self, request: HttpRequest, post_id):
        try:
            # Get requested post
            current_user = request.user
            post = Post.objects.get(id=post_id, user__username=current_user.username)

            # Delete it
            post.delete()

            messages.success(request, "The post has been deleted successfully")
            return redirect("app:home")

        except ObjectDoesNotExist:
            raise Http404()
        except Exception as e:
            if settings.DEBUG:
                raise e
            return HttpResponseServerError()
