from django.shortcuts import render
from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    extra_context = {
        'page_title': "Login"
    }
