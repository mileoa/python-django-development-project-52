from django.urls import path
from statuses.views import (
    IndexStatusView,
    CreateStatusView,
    UpdateStatusView,
    DeleteStatusView,
)

urlpatterns = [
    path("", IndexStatusView.as_view(), name="status_list"),
    path("create/", CreateStatusView.as_view(), name="status_create"),
    path("<int:pk>/update/", UpdateStatusView.as_view(), name="status_update"),
    path("<int:pk>/delete/", DeleteStatusView.as_view(), name="status_delete"),
]
