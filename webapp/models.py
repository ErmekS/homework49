from django.db import models

# Create your models here.

STATUS_CHOICES = [('new', 'Новая'), ('in_progress', 'В процессе'), ('done', 'Сделано')]
TYPE_CHOICES = [('task', 'Задача'), ('bug', 'Ошибка'), ('enhancement', 'Улучшение')]


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Status(models.Model):
    status = models.CharField(max_length=35, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.get_status_display()}'

    class Meta:
        db_table = "status"
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    type = models.CharField(max_length=35, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.get_type_display()}'

    class Meta:
        db_table = "types"
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Sketchpad(BaseModel):
    summary = models.CharField(max_length=50, null=False, blank=False, default="No summary",
                               verbose_name="Краткое описание")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Полное описание")
    status = models.ForeignKey("webapp.Status", on_delete=models.PROTECT, related_name='statuses',
                               verbose_name='Статус')
    type = models.ForeignKey("webapp.Type", on_delete=models.PROTECT, related_name="issues", verbose_name='Тип')

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.status} {self.description} {self.created_time}"

    class Meta:
        db_table = "sketchpad"
        verbose_name = "задача"
        verbose_name_plural = "Список задач"
