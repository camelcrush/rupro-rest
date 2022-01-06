from django.db import models
from core.models import CoreModel


class Board(CoreModel):

    content = models.TextField(max_length=200)
    game = models.ForeignKey(
        "games.Game", related_name="boards", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="boards"
    )

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-pk"]
