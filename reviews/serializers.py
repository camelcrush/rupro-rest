from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "reviewed_game_score",
            "review",
            "rating_average",
            "manner",
            "attitude",
            "humor",
            "physical",
            "sense",
        )
        read_only_fields = ("id", "user", "rating_average")

    def create(self, validated_data):
        request = self.context.get("request")
        review = Review.objects.create(**validated_data, user=request.user)
        return review
