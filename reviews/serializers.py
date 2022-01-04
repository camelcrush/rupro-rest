from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "review",
            "manner",
            "attitude",
            "humor",
            "physical",
            "sense",
            "user",
            "game_score",
            "rating_average",
        )
        read_only_fields = ("user", "game_score", "rating_average")

    def create(self, validated_data):
        request = self.context.get("request")
        review = Review.objects.create(**validated_data, user=request.user)
        return review
