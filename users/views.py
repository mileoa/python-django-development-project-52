from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
)

from .models import User
from .forms import UserForm


# Create your views here.
class IndexUserView(ListView):

    http_method_names = ["get"]
    model = User
    context_object_name = "users"


class CreateUserView(SuccessMessageMixin, CreateView):

    http_method_names = ["get", "post"]
    form_class = UserForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UpdateUserView(SuccessMessageMixin, UpdateView):

    http_method_names = ["get", "post"]
    model = User
    form_class = UserForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("user_list")
    success_message = "Пользователь успешно изменен"


class DeleteUserView(SuccessMessageMixin, DeleteView):

    http_method_names = ["get", "post"]
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("user_list")
    success_message = "Пользователь успешно удален"
