from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'is_superuser', 'is_staff', 'role')
    search_fields = ('username',)
    list_filter = ('is_staff', 'role')
    list_editable = ('is_superuser', 'is_staff', 'role')
    empty_value_display = '-пусто-'