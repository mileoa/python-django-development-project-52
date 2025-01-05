from django.db import models
from statuses.models import Statuses
from users.models import Users


# Create your models here.
class Tasks(models.Model):

    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(
        Statuses, on_delete=models.PROTECT, related_name="status", verbose_name="Статус"
    )
    author = models.ForeignKey(
        Users, on_delete=models.PROTECT, related_name="author", verbose_name="Автор"
    )
    executor = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="executor",
        verbose_name="Исполнитель",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name
