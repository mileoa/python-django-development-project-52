from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
)

from .models import Users
from .forms import UserForm
from task_manager.constants import (
    PERMISSION_DENIED_NO_LOGIN_MESSAGE,
    PERMISSION_DENIED_NO_RIGHTS_MESSAGE,
)


class IndexUserView(ListView):

    http_method_names = ["get"]
    model = Users
    context_object_name = "users"


class CreateUserView(SuccessMessageMixin, CreateView):

    # CreateView
    http_method_names = ["get", "post"]
    form_class = UserForm
    template_name = "users/users_create.html"
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


class UpdateUserView(
    DeleteUpdateUserRulesMixin, SuccessMessageMixin, UpdateView
):

    # UpdateView
    http_method_names = ["get", "post"]
    model = Users
    form_class = UserForm
    template_name = "users/users_update.html"
    success_url = reverse_lazy("user_list")
    # SuccessMessageMixin
    success_message = "Пользователь успешно изменен"


class DeleteUserView(
    DeleteUpdateUserRulesMixin, SuccessMessageMixin, DeleteView
):

    # DeleteView
    http_method_names = ["get", "post"]
    model = Users
    template_name = "users/users_delete.html"
    success_url = reverse_lazy("user_list")

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            messages.add_message(
                request, messages.SUCCESS, "Пользователь успешно удален"
            )
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            messages.add_message(
                request,
                messages.ERROR,
                "Невозможно удалить пользователя, потому что он используется",
            )
            return HttpResponseRedirect(reverse_lazy("task_list"))
