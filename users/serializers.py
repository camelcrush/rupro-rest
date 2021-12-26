from rest_framework import serializers
from relations.serializers import RelationSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    relations = RelationSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "tier",
            "bio",
            "relations",
            "password",
        )
        read_only_fields = ("id", "avatar", "tier")

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance
