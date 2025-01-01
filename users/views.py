from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView

from .models import User
from .forms import UserCreateForm


# Create your views here.
class IndexUserView(ListView):

    http_method_names = ["get"]
    model = User
    context_object_name = "users"


class CreateUserView(CreateView):

    form_class = UserCreateForm
    template_name = "users/user_create.html"
    http_method_names = ["get", "post"]
    success_url = reverse_lazy("user_list")
    success_message = "Пользователь успешно зарегистрирован"


class UpdateUserView(UpdateView):

    http_method_names = ["get", "post"]
    model = User


class DeleteUserView(TemplateView):

    http_method_names = ["post"]
    model = User
