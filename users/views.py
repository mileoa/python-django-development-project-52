from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from .models import User


# Create your views here.
class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, "users/index.html", context={"users": users})


class UpdateView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, "users/update.html", context={})

    def post(self, request, *args, **kwargs):
        return render(request, "users/update.html", context={})


class DeleteView(TemplateView):

    def post(self, request, *args, **kwargs):
        return redirect("users_index")
