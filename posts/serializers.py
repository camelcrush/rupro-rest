from rest_framework import serializers
from .models import Photo, Post


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "file")


class PostSerializer(serializers.ModelSerializer):

    is_like = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated", "photos")

    def get_is_like(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.likes.all()
        return False

    def create(self, validated_data):
        request = self.context.get("request")
        photos = request.FILES
        post = Post.objects.create(**validated_data, user=request.user)
        for photo in photos.getlist("file"):
            Photo.objects.create(file=photo, post=post)
        return post
