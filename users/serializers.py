from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_name",
            "email",
            "avatar",
            "tier",
            "bio",
            "blocked_user",
            "following_user",
            "followers",
            "game_list",
            "password",
        )
        read_only_fields = ("id", "tier", "followers")

    def get_followers(self, obj):
        user = obj.user
        return TinyUserSerializer(user.followers.all(), many=True).data

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
