from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
)

from .models import User
from .forms import UserForm

PERMISSION_DENIED_NO_LOGIN_MESSAGE = "Вы не авторизованы! Пожалуйста, выполните вход."
PERMISSION_DENIED_NO_RIGHTS_MESSAGE = (
    "У вас нет прав для изменения другого пользователя."
)


class IndexUserView(ListView):

    http_method_names = ["get"]
    model = User
    context_object_name = "users"


class CreateUserView(SuccessMessageMixin, CreateView):

    # CreateView
    http_method_names = ["get", "post"]
    form_class = UserForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("login")
    # SuccessMessageMixin
    success_message = "Пользователь успешно зарегистрирован"


class DeleteUpdateUserRulesMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, PERMISSION_DENIED_NO_LOGIN_MESSAGE
            )
            return redirect(reverse_lazy("login"))
        if request.user.pk != kwargs.get("pk"):
            messages.add_message(
                request, messages.ERROR, PERMISSION_DENIED_NO_RIGHTS_MESSAGE
            )
            return redirect(reverse_lazy("user_list"))
        return super().dispatch(request, *args, **kwargs)


class UpdateUserView(DeleteUpdateUserRulesMixin, SuccessMessageMixin, UpdateView):

    # UpdateView
    http_method_names = ["get", "post"]
    model = User
    form_class = UserForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("user_list")
    # SuccessMessageMixin
    success_message = "Пользователь успешно изменен"


class DeleteUserView(DeleteUpdateUserRulesMixin, SuccessMessageMixin, DeleteView):

    # DeleteView
    http_method_names = ["get", "post"]
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("user_list")
    # SuccessMessageMixin
    success_message = "Пользователь успешно удален"
