from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Sketchpad, Project


class SketchpadForm(forms.ModelForm):
    class Meta:
        model = Sketchpad
        fields = ["summary", "description", "type", "status"]
        widgets = {
            "type": widgets.CheckboxSelectMultiple
        }

        def clean(self):
            if self.cleaned_data.get("summary") == self.cleaned_data.get("description"):
                raise ValidationError("Краткий заголовок и описание не могут совпадать")
            return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Поиск')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'start_date', 'expiration_date']
        widgets = {
            "project_description": widgets.Textarea(attrs={"placeholder": "Введите описание"}),
            "start_date": widgets.DateInput(attrs={'placeholder': "Формат: год-месяц-день"}),
            "expiration_date": widgets.DateInput(attrs={'placeholder': "Формат: год-месяц-день"})
        }

        def clean(self):
            if self.cleaned_data.get("project_name") == self.cleaned_data.get("project_description"):
                raise ValidationError("Название и описание проекта не могут совпадать")
            return super().clean()

