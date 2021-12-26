from rest_framework import serializers
from django.core import serializers as serializer
from .models import Relation
from users.models import User


class RelationSerializer(serializers.ModelSerializer):

    followers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Relation
        fields = ("following_user", "followers", "blocked_user")
        read_only_fields = ("followers",)

    def get_followers(self, obj):
        user = obj.user
        return FollowersSerializer(user.followers.all(), many=True).data


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ("user",)
