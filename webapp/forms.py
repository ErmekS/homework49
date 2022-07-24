from django import forms
from django.forms import widgets
from webapp.models import Sketchpad, Status, Type

from webapp.validate import bad_words, bad_chars, check_count


class SketchpadForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, validators=(bad_chars,))
    description = forms.CharField(max_length=2000, validators=(bad_words,),
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), validators=(check_count,),
                                          widget=forms.CheckboxSelectMultiple)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label='')

    class Meta:
        model = Sketchpad
        fields = '__all__'
