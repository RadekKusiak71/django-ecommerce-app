from typing import Any
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.template.response import TemplateResponse
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from store.forms import RegisterForm
from django.urls import reverse_lazy


class RegisterCreateView(generic.CreateView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("login-page")


class LoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy("home-page")
    next_page = reverse_lazy("home-page")


class LogoutView(LogoutView):
    template_name = 'auth/logout.html'
    next = reverse_lazy("login-page")
