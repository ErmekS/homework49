from django import forms
from django.forms import widgets
from webapp.models import Sketchpad, Status, Type

STATUS_CHOICES = [('new', 'Новая'), ('in_progress', 'В процессе'), ('done', 'Сделано')]
TYPE_CHOICES = [('task', 'Задача'), ('bug', 'Ошибка'), ('enhancement', 'Улучшение')]


class SketchpadForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, required=True, label='Краткое описание')
    description = forms.CharField(max_length=2000, required=False, label='Полное описание',
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, label='Тип')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label=None, required=True, label='Статус')

    class Meta:
        model = Sketchpad
        fields = '__all__'
