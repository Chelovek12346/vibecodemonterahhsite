from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ("username", "email", "first_name", "last_name", "school", "grade", "gpa", "is_staff")
    list_filter   = ("is_staff", "is_superuser", "is_active", "grade")
    search_fields = ("username", "email", "first_name", "last_name", "school")
    ordering      = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Личные данные", {"fields": ("first_name", "last_name", "email", "school", "grade", "gpa")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "school", "grade", "gpa", "password1", "password2"),
        }),
    )
