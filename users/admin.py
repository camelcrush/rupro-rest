from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "tier",
                    "gender",
                    "bio",
                    "blocked_user",
                    "following_user",
                    "game_list",
                    "login_method",
                )
            },
        ),
    )

    list_display = UserAdmin.list_display + ("gender", "tier", "login_method")
