from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users


class UserForm(UserCreationForm):

    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(
        label="Имя пользователя",
        help_text="Обязательное поле. Не более 150 символов."
        "Только буквы, цифры и символы @/./+/-/_.",
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Ваш пароль должен содержать как минимум 3 символа.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.",
    )

    class Meta:
        model = Users
        fields = ["first_name", "last_name", "username"]
