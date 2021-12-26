from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated")

    def create(self, validated_data):
        request = self.context.get("request")
        post = Post.objects.create(**validated_data, user=request.user)
        return post
