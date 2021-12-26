from rest_framework import serializers
from .models import UserGameScoreModel


class UserGameScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameScoreModel
        fields = (
            "user",
            "game",
            "manner",
            "attitude",
            "humor",
            "physical",
            "sense",
        )
