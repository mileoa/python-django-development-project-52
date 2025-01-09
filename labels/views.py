from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from task_manager.constants import PERMISSION_DENIED_NO_LOGIN_MESSAGE
from .forms import LabelsForm
from .models import Labels


class CommonLabelMixin(LoginRequiredMixin, SuccessMessageMixin):

    login_url = reverse_lazy("login")
    model = Labels

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, PERMISSION_DENIED_NO_LOGIN_MESSAGE
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IndexLabelView(CommonLabelMixin, ListView):

    http_method_names = ["get"]
    context_object_name = "labels"


class CreateLabelView(CommonLabelMixin, CreateView):

    # CreateView
    http_method_names = ["get", "post"]
    template_name = "labels/labels_create.html"
    success_url = reverse_lazy("label_list")
    form_class = LabelsForm
    # SuccessMessageMixin
    success_message = "Метка успешно создана"


class UpdateLabelView(CommonLabelMixin, UpdateView):

    # UpdateView
    http_method_names = ["get", "post"]
    template_name = "labels/labels_update.html"
    success_url = reverse_lazy("label_list")
    form_class = LabelsForm
    context_object_name = "label"
    # SuccessMessageMixin
    success_message = "Метка успешно изменена"


class DeleteLabelView(CommonLabelMixin, DeleteView):

    # DeleteView
    http_method_names = ["get", "post"]
    template_name = "labels/labels_delete.html"
    context_object_name = "label"
    success_url = reverse_lazy("label_list")

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            messages.add_message(
                request, messages.SUCCESS, "Метка успешно удалена"
            )
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            messages.add_message(
                request,
                messages.ERROR,
                "Невозможно удалить метку, потому что она используется",
            )
            return HttpResponseRedirect(reverse_lazy("label_list"))
