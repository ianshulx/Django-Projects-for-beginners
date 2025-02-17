from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Profile


# Reference : UserAdmin class [ https://github.com/django/django/blob/main/django/contrib/auth/admin.py ]
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    # Controls which fields are displayed on the change list page of the admin
    list_display = [
        "id",
        "email",
        "username",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]

    # Tuples defined for different sections of the UserCreationForm and UserChangeForm
    permissions = (
        _("Permissions"),
        {
            "fields": ("is_active", "is_staff", "is_superuser"),
        },
    )
    personal_info = (
        _("Personal info"),
        {
            "classes": ("collapse",),
            "fields": (
                "username",
                "first_name",
                "last_name",
                "date_joined",
            ),
        },
    )
    advanced_permissions = (
        _("Advanced Permissions"),
        {
            "classes": ("collapse",),
            "fields": ("groups", "user_permissions"),
        },
    )

    # Notes: Fieldsets control the layout of admin "add" and "change" pages.
    #   Fieldsets = One or more fieldset.
    #   Fieldset = (name, field_options)
    #   ---------------------------------
    # Fields for UserChangeForm
    fieldsets = [
        (
            _("Modify User"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        permissions,
        personal_info,
        advanced_permissions,
    ]

    # Notes : add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # Fields for UserCreationForm
    add_fieldsets = [
        (
            _("Create User"),
            {
                "fields": ("email", "password1", "password2", "username"),
            },
        ),
        permissions,
        personal_info,
        advanced_permissions,
    ]

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "displayname", "info"]
    search_fields = ["user__username", "displayname", "info"]
