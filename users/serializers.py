from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from .models import User
from .tokens import account_activation_token


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
            "first_name",
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

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이메일이 이미 존재합니다.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("패스워드는 8자 이상이여야 합니다.")
        return value

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.email = user.username
        user.save()

        current_site = get_current_site(self.context.get("request"))
        message = render_to_string(
            "emails/verify_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk))
                .encode()
                .decode("utf-8"),
                "token": account_activation_token.make_token(user),
            },
        )
        mail_subject = "Verify Your Account."
        email = EmailMessage(mail_subject, strip_tags(message), to=[user.username])
        email.send()
        return user
