from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from users.models import User


class UserAdmin(BaseUserAdmin):

    list_display = (
        'username', 'pk', 'role', 'email', 'first_name'
    )
    search_fields = ('username', 'role')
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
