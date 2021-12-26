from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import CoreModel


class User(AbstractUser):

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMANLE = "female"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMANLE, "Female"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GOOGLE = "google"
    LOGIN_KAKAO = "kakao"
    LOGIN_FACEBOOK = "facebook"
    LOGIN_APPLE = "apple"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GOOGLE, "Google"),
        (LOGIN_KAKAO, "Kakao"),
        (LOGIN_FACEBOOK, "FaceBook"),
        (LOGIN_APPLE, "Apple"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    tier = models.CharField("tier", max_length=20, blank=True)
    gender = models.CharField(
        "gender", choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField("bio", max_length=200, blank=True)
    login_method = models.CharField(
        max_length=80, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    likes = models.ManyToManyField("posts.Post", related_name="likes", blank=True)
    following_user = models.ManyToManyField(
        "users.User", related_name="followers", symmetrical=False, blank=True
    )
    blocked_user = models.ManyToManyField(
        "users.User", related_name="blocked_users", symmetrical=False, blank=True
    )
    game_list = models.ManyToManyField("games.Game", blank=True)

    class Meta:
        ordering = ["-pk"]
