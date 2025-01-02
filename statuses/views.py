from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from task_manager.constants import PERMISSION_DENIED_NO_LOGIN_MESSAGE
from .models import Statuses


class CommonStatusMixin(LoginRequiredMixin, SuccessMessageMixin):

    login_url = reverse_lazy("login")
    model = Statuses

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, PERMISSION_DENIED_NO_LOGIN_MESSAGE
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IndexStatusView(CommonStatusMixin, ListView):

    http_method_names = ["get"]
    context_object_name = "statuses"


class CreateStatusView(CommonStatusMixin, CreateView):

    # CreateView
    http_method_names = ["get", "post"]
    template_name = "statuses/statuses_create.html"
    success_url = reverse_lazy("status_list")
    fields = ["name"]
    # SuccessMessageMixin
    success_message = "Статус успешно создан"


class UpdateStatusView(CommonStatusMixin, UpdateView):

    # UpdateView
    http_method_names = ["get", "post"]
    template_name = "statuses/statuses_update.html"
    success_url = reverse_lazy("status_list")
    fields = ["name"]
    context_object_name = "status"
    # SuccessMessageMixin
    success_message = "Статус успешно изменен"


class DeleteStatusView(CommonStatusMixin, DeleteView):

    # DeleteView
    http_method_names = ["get", "post"]
    template_name = "statuses/statuses_delete.html"
    context_object_name = "status"
    success_url = reverse_lazy("status_list")

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            messages.add_message(request, messages.SUCCESS, "Статус успешно удален")
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            messages.add_message(
                request,
                messages.ERROR,
                "Невозможно удалить статус, потому что он используется",
            )
            return HttpResponseRedirect(reverse_lazy("status_list"))
