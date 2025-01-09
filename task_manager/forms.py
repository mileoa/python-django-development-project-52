from django import forms
from django.contrib.auth.forms import AuthenticationForm
from users.models import Users


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )

    class Meta:
        model = Users
        fields = ["username", "password"]
