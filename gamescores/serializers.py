from rest_framework import serializers
from .models import GameScore
from reviews.serializers import ReviewSerializer
from games.serializers import GameSerializer


class GameScoreSerializer(serializers.ModelSerializer):

    is_active = serializers.SerializerMethodField()
    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = GameScore
        fields = (
            "id",
            "user",
            "game",
            "is_active",
            "total_rating",
            "manner_rating",
            "attitude_rating",
            "humor_rating",
            "physical_rating",
            "sense_rating",
            "reviews",
        )
        read_only_fields = (
            "user",
            "is_active",
            "total_rating",
            "manner_rating",
            "attitude_rating",
            "humor_rating",
            "physical_rating",
            "sense_rating",
            "reviews",
        )

    def get_is_active(self, obj):
        user = obj.user
        return obj.game in user.game_list.all()

    def create(self, validated_data):
        request = self.context.get("request")
        game = validated_data.get("game")
        user = request.user
        user.game_list.add(game)
        game_score = GameScore.objects.create(**validated_data, user=user)
        return game_score
