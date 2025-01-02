from django.contrib.auth.forms import UserCreationForm
from .models import Users


class UserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ["first_name", "last_name", "username"]
