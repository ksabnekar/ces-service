from django.contrib import admin
from django.contrib.auth.models import User

class UserList(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')


admin.site.register(User, UserList)
