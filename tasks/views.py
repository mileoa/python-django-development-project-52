from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from task_manager.constants import PERMISSION_DENIED_NO_LOGIN_MESSAGE
from .models import Tasks
from .forms import TasksForm


class CommonTaskMixin(LoginRequiredMixin, SuccessMessageMixin):

    login_url = reverse_lazy("login")
    model = Tasks

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, PERMISSION_DENIED_NO_LOGIN_MESSAGE
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IndexTaskView(CommonTaskMixin, ListView):

    http_method_names = ["get"]
    context_object_name = "tasks"


class DetailTaskView(CommonTaskMixin, DetailView):

    context_object_name = "task"


class CreateTaskView(CommonTaskMixin, CreateView):

    # CreateView
    http_method_names = ["get", "post"]
    template_name = "tasks/tasks_create.html"
    success_url = reverse_lazy("task_list")
    form_class = TasksForm
    # SuccessMessageMixin
    success_message = "Задача успешно создана"


class UpdateTaskView(CommonTaskMixin, UpdateView):

    # UpdateView
    http_method_names = ["get", "post"]
    template_name = "tasks/tasks_update.html"
    success_url = reverse_lazy("task_list")
    form_class = TasksForm
    context_object_name = "task"
    # SuccessMessageMixin
    success_message = "Задача успешно изменена"


class DeleteTaskView(CommonTaskMixin, DeleteView):

    # DeleteView
    http_method_names = ["get", "post"]
    template_name = "tasks/tasks_delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("task_list")

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()

            if self.object.author.pk != self.request.user.pk:
                messages.add_message(
                    request, messages.ERROR, "Задачу может удалить только ее автор"
                )
                return HttpResponseRedirect(reverse_lazy("task_list"))

            self.object.delete()
            messages.add_message(request, messages.SUCCESS, "Задача успешно удалена")
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            messages.add_message(
                request,
                messages.ERROR,
                "Невозможно удалить задачу, потому что она используется",
            )
            return HttpResponseRedirect(reverse_lazy("task_list"))
