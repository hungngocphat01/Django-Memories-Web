from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request: HttpRequest):
        current_user = request.user
        return render(request, self.template_name, {
            'title': 'Home',
            'current_user': current_user
        })

class LoginView(View):
    template_name = 'home/login.html'

    def get(self, request: HttpRequest):
        current_user = request.user
        return render(request, self.template_name, {
            'title': 'Login',
            'current_user': current_user
        })

class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('app:login')