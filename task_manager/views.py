from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy


class MainIndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "Вы залогинены"


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = "Вы разлогинены"
