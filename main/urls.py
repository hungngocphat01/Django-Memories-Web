from django.urls import path 
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'app'

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('post_cr', login_required(PostCreateEditView.as_view()), name='post_create_edit')
]