from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта', required=True, widget=forms.EmailInput)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name == '' and last_name == '':
            raise ValidationError("Введите Имя или Фамилию")

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
