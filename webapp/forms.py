from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Sketchpad


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
