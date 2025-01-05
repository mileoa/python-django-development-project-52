import django_filters
from django import forms
from .models import Tasks
from labels.models import Labels


class TasksFilter(django_filters.FilterSet):

    self_tasks = django_filters.BooleanFilter(
        "id",
        method="filter_self_tasks",
        label="Только свои задачи",
        widget=forms.CheckboxInput(),
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(), label="Метка"
    )

    class Meta:
        model = Tasks
        fields = ["status", "executor", "labels", "self_tasks"]

    def filter_self_tasks(self, queryset, name, is_only_self):
        if not is_only_self:
            return queryset
        if self.request is None:
            return Tasks.objects.none()
        return queryset.filter(author=self.request.user)
