from django.contrib import admin
from . import models


@admin.register(models.Relation)
class UserFollowingAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "info",
            {
                "fields": (
                    "user",
                    "following_user",
                    "blocked_user",
                ),
            },
        ),
    )
