# coding: utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_per_page = 30
    search_fields = ("email",)
    list_display = (
        "email",
        "date_joined",
        "last_login",
    )
    readonly_fields = (
        "last_login",
        "date_joined",
    )
