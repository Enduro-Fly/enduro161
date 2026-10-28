from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import zayavka

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': 'Имя пользователя', 'password1': 'Пароль', 'password2': 'Повторите пароль'}
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Ваше имя'}), 'password1': forms.PasswordInput(), 'password2': forms.PasswordInput()}

class CreateZayavkaForm(forms.ModelForm):
    class Meta:
        model = zayavka
        fields = ['type', 'datetime', 'hours', 'payment']
        labels = {'type': 'Выберите мотоцикл', 'datetime': 'Дата и время начала', 'hours': 'На сколько часов', 'payment': 'Способ оплаты'}
        widgets = {'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}), 'hours': forms.Select(choices=[(1, '1 час'), (2, '2 часа'), (3, '3 часа'), (4, '4 часа'), (6, '6 часов'), (8, 'Весь день — 8 часов')])}

    def clean_datetime(self):
        value = self.cleaned_data['datetime']
        if value <= timezone.now():
            raise forms.ValidationError('Выберите дату и время в будущем.')
        return value
