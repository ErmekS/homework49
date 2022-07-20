from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


STATUS_CHOICES = [('new', 'Новая'), ('in_progress', 'В процессе'), ('done', 'Сделано')]
TYPE_CHOICES = [('task', 'Задача'), ('bug', 'Ошибка'), ('enhancement', 'улучшение')]


class Sketchpad(BaseModel):
    summary = models.CharField(max_length=50, null=False, blank=False, default="No summary",
                               verbose_name="Краткое описание")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Полное описание")
    status = models.CharField(max_length=20, on_delete=models.PROTECT, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0],
                              verbose_name="Статус")
    type = models.CharField(max_length=20, on_delete=models.PROTECT, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
                            verbose_name="Тип")

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.status} {self.description} {self.created_time}"

    class Meta:
        db_table = "sketchpad"
        verbose_name = "задача"
        verbose_name_plural = "Список задач"
