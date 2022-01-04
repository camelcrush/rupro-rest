from django.db import models
from core.models import CoreModel


class GameScore(CoreModel):

    user = models.OneToOneField(
        "users.User", related_name="game_scores", on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        "games.Game", related_name="user_scores", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} - {self.game}"

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def manner_rating(self):
        all_reviews = self.reviews.all()
        manner_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                manner_ratings += review.manner
            return round(manner_ratings / len(all_reviews), 2)
        return 0

    def attitude_rating(self):
        all_reviews = self.reviews.all()
        attitude_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                attitude_ratings += review.attitude
            return round(attitude_ratings / len(all_reviews), 2)
        return 0

    def humor_rating(self):
        all_reviews = self.reviews.all()
        humor_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                humor_ratings += review.humor
            return round(humor_ratings / len(all_reviews), 2)
        return 0

    def physical_rating(self):
        all_reviews = self.reviews.all()
        physical_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                physical_ratings += review.physical
            return round(physical_ratings / len(all_reviews), 2)
        return 0

    def sense_rating(self):
        all_reviews = self.reviews.all()
        sense_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                sense_ratings += review.sense
            return round(sense_ratings / len(all_reviews), 2)
        return 0

    class Meta:
        ordering = ["-pk"]
