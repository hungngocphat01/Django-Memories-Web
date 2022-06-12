from django.urls import path 
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('post', PostCreateView.as_view(), name='post_create'),
    path('post/<str:post_id>', PostView.as_view(), name='post_view'),
    path('post/<str:post_id>/edit', PostEditView.as_view(), name='post_edit'),
    path('post/<str:post_id>/delete', PostDelete.as_view(), name='post_delete'),
]