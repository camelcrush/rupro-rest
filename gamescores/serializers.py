from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import GameScore
from reviews.serializers import ReviewSerializer
from games.models import Game


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

    def create(self, validated_data):
        request = self.context.get("request")
        game_pk = validated_data.get("game")
        print(game_pk)
        try:
            game = Game.objects.filter(pk=game_pk)
            game_score = GameScore.objects.create(user=request.user, game=game)
            return game_score
        except Game.DoesNotExist:
            raise serializers.ValidationError("해당 게임이 없습니다.")

    def get_is_active(self, obj):
        user = obj.user
        return obj.game in user.game_list.all()
