from django.db import models


# Create your models here.
class Statuses(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self):
        return self.name
