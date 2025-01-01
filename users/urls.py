from django.urls import path
from users.views import IndexUserView, UpdateUserView, DeleteUserView, CreateUserView

urlpatterns = [
    path("", IndexUserView.as_view(), name="user_list"),
    path("create/", CreateUserView.as_view(), name="user_create"),
    path("<int:pk>/update/", UpdateUserView.as_view(), name="user_update"),
    path("<int:pk>/delete/", DeleteUserView.as_view(), name="user_delete"),
]
