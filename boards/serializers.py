from rest_framework import serializers
from .models import Board


class BoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated")

    def create(self, validated_data):
        request = self.context.get("request")
        board = Board.objects.create(**validated_data, user=request.user)
        return board
