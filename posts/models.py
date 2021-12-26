from django.db import models
from core.models import CoreModel


class Post(CoreModel):

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    game = models.ForeignKey(
        "games.Game", related_name="posts", on_delete=models.SET_NULL, null=True
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pk"]


class Photo(CoreModel):

    file = models.ImageField(upload_to="posts", blank=True, null=True)
    post = models.ForeignKey(
        "posts.Post", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.post.name
