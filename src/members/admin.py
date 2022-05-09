# coding: utf-8

from django.contrib import admin

from members.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_select_related = ("user",)
    search_fields = ("user__email",)
    list_display = (
        "user",
        "name",
        "function",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "user",
    )
