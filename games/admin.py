from django.contrib import admin
from . import models


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "kind",
    )
