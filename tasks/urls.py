from django.urls import path
from tasks.views import (
    IndexTaskView,
    CreateTaskView,
    UpdateTaskView,
    DeleteTaskView,
    DetailTaskView,
)

urlpatterns = [
    path("", IndexTaskView.as_view(), name="task_list"),
    path("<int:pk>/", DetailTaskView.as_view(), name="task_detail"),
    path("create/", CreateTaskView.as_view(), name="task_create"),
    path("<int:pk>/update/", UpdateTaskView.as_view(), name="task_update"),
    path("<int:pk>/delete/", DeleteTaskView.as_view(), name="task_delete"),
]
