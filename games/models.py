from django.db import models
from core.models import CoreModel


class Game(CoreModel):

    GAME_LOL = "legue of legent"
    GAME_BAT = "battleground"
    GAME_DIA2 = "diablo2"

    LOGIN_CHOICES = (
        (GAME_LOL, "League Of Legend"),
        (GAME_BAT, "BattleGround"),
        (GAME_DIA2, "Diablo2"),
    )

    name = models.CharField(max_length=140, choices=LOGIN_CHOICES)
    kind = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-pk"]
