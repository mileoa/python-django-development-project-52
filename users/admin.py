from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Users

# Register your models here.
admin.site.register(Users, UserAdmin)
