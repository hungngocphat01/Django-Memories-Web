from django.urls import path 
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'app'

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('post', login_required(PostCreateView.as_view()), name='post_create'),
    path('post/<str:post_id>', login_required(PostView.as_view()), name='post_view'),
    path('post/<str:post_id>/edit', login_required(PostEditView.as_view()), name='post_edit'),
    path('post/<str:post_id>/delete', login_required(PostDelete.as_view()), name='post_delete'),
]