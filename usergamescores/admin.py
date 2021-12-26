from django.contrib import admin
from .models import UserGameScoreModel


@admin.register(UserGameScoreModel)
class UserGameScoreAdmin(admin.ModelAdmin):

    list_display = (
        "game",
        "user",
        "manner",
        "attitude",
        "humor",
        "physical",
        "sense",
    )
