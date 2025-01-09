from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django_filters.views import FilterView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.constants import PERMISSION_DENIED_NO_LOGIN_MESSAGE
from .models import Tasks
from .forms import TasksForm
from .filters import TasksFilter


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


class IndexTaskView(CommonTaskMixin, FilterView):

    http_method_names = ["get"]
    context_object_name = "tasks"
    filterset_class = TasksFilter


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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(CommonTaskMixin, UpdateView):

    # UpdateView
    http_method_names = ["get", "post"]
    template_name = "tasks/tasks_update.html"
    success_url = reverse_lazy("task_list")
    form_class = TasksForm
    context_object_name = "task"
    # SuccessMessageMixin
    success_message = "Задача успешно изменена"


class DeleteTaskView(LoginRequiredMixin, DeleteView):

    # DeleteView
    http_method_names = ["get", "post"]
    template_name = "tasks/tasks_delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("task_list")
    login_url = reverse_lazy("login")
    model = Tasks

    def has_permission(self) -> bool:
        return self.get_object().author.pk == self.request.user.pk

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, PERMISSION_DENIED_NO_LOGIN_MESSAGE
            )
            return self.handle_no_permission()
        if not self.has_permission():
            messages.error(request, "Задачу может удалить только ее автор")
            return HttpResponseRedirect(reverse_lazy("task_list"))
        return super().dispatch(request, *args, **kwargs)
