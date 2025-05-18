from django import forms
from .models import Folio
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FolioForm(forms.ModelForm):
    class Meta:
        model = Folio
        fields = ['name', 'description']
        labels = {
            'name': 'Название портфеля',
            'description': 'Описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя'
    )
    email = forms.EmailField(
        label='Email-адрес'
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        strip=False
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]