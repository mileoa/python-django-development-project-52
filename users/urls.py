from django.urls import path
from users.views import IndexView, UpdateView, DeleteView

urlpatterns = [
    path("", IndexView.as_view(), name="users_index"),
    path("update/", UpdateView.as_view(), name="users_update"),
    path("delete/", DeleteView.as_view(), name="users_delete"),
]
