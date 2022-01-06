from django.db import models
from core.models import CoreModel


class Game(CoreModel):

    name = models.CharField(max_length=30)
    kind = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-pk"]
