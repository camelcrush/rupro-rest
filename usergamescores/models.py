from django.db import models
from core.models import CoreModel


class UserGameScoreModel(CoreModel):

    game = models.ForeignKey(
        "games.Game", related_name="user_scores", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="game_scores", on_delete=models.CASCADE
    )
    manner = models.IntegerField("manner", blank=True)
    attitude = models.IntegerField("attitude", blank=True)
    humor = models.IntegerField("humor", blank=True)
    physical = models.IntegerField("physical", blank=True)
    sense = models.IntegerField("sense", blank=True)

    class Meta:
        ordering = ["-pk"]
