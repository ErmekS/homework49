from django.db import models

# Create your models here.
from django.urls import reverse

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
        return f'{self.status}'

    class Meta:
        db_table = "status"
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    type = models.CharField(max_length=35, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.type}'

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
    type = models.ManyToManyField("webapp.Type", related_name="issues", verbose_name='Тип')
    project = models.ForeignKey("webapp.Project", on_delete=models.CASCADE, related_name="projects",
                                verbose_name='Проект')


    def __str__(self):
        return f"{self.id}. {self.summary}"

    class Meta:
        db_table = "sketchpad"
        verbose_name = "задача"
        verbose_name_plural = "Список задач"

class Project(models.Model):
    start_date = models.DateField(verbose_name="Дата начала")
    expiration_date = models.DateField(null=True, blank=True,
                                       verbose_name="Дата окончания")
    project_name = models.CharField(max_length=35, verbose_name="Название проекта")
    project_description = models.TextField(max_length=3000, verbose_name="Описание проекта")

    def __str__(self):
        return f"{self.id}. {self.project_name}"

    def get_absolute_url(self):
        return reverse("ProjectView", kwargs={"pk": self.pk})

    class Meta:
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"