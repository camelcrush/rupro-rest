from django.db import models
from core.models import CoreModel


class Relation(CoreModel):

    user = models.OneToOneField(
        "users.User", related_name="relations", on_delete=models.CASCADE
    )

    following_user = models.ManyToManyField(
        "users.User", related_name="followers", symmetrical=False, blank=True
    )
    blocked_user = models.ManyToManyField(
        "users.User", related_name="blocked_users", symmetrical=False, blank=True
    )
    my_game_list = models.ManyToManyField("games.Game", blank=True)

    class Meta:

        ordering = ["-created"]

    def __str__(self):
        return f"{self.user}'s Relations"
