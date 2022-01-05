from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import CoreModel


class Review(CoreModel):

    review = models.TextField(max_length=200)
    manner = models.IntegerField(
        "manner", validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
    attitude = models.IntegerField(
        "attitude", validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
    humor = models.IntegerField(
        "humor", validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
    physical = models.IntegerField(
        "physical", validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
    sense = models.IntegerField(
        "sense", validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    reviewed_game_score = models.ForeignKey(
        "gamescores.GameScore", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.reviewed_game_score}"

    def rating_average(self):
        avg = (
            self.manner + self.attitude + self.humor + self.physical + self.sense
        ) / 5
        return round(avg, 2)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)
