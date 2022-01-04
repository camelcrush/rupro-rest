from rest_framework import serializers
from .models import GameScore


class GameScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScore
        fields = (
            "user",
            "game",
            "total_rating",
            "manner_rating",
            "attitude_rating",
            "humor_rating",
            "physical_rating",
            "sense_rating",
        )
