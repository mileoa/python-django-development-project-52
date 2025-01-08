from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from task_manager.forms import CustomLoginForm


class MainIndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "Вы залогинены"
    form_class = CustomLoginForm


class CustomLogoutView(SuccessMessageMixin, LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
