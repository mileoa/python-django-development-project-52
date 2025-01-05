from django.db import models


# Create your models here.
class Labels(models.Model):

    name = models.CharField(max_length=100, verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name
