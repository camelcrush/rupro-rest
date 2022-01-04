from django.contrib import admin
from .models import GameScore


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "total_rating",
        "manner_rating",
        "attitude_rating",
        "humor_rating",
        "physical_rating",
        "sense_rating",
    )
