from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    search_fields = [
        "email",
        "username",
        "first_name",
        "last_name",
    ]

    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal Info"),
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")},
        ),
    )

    add_fieldsets = (
        (
            _("User Information"),
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                ),
            },
        ),
        (
            _("Password"),
            {
                "classes": ("wide",),
                "fields": (
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
