from games.serializers import GameSerializer
from posts.models import Post
from posts.serializers import PostSerializer
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, TinyUserSerializer
from .models import User
from games.models import Game
from games.serializers import GameSerializer
from .permissions import IsSelf


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        if (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "likes"
            or self.action == "blocks"
            or self.action == "follows"
            or self.action == "game_lists"
        ):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf | IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def likes(self, request, pk):
        user = self.get_object()
        serializer = PostSerializer(
            user.likes.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    @likes.mapping.put
    def toggle_likes(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if request.user != user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if pk is not None:
            try:
                post = Post.objects.get(pk=pk)
                if post in user.likes.all():
                    user.likes.remove(post)
                else:
                    user.likes.add(post)
                return Response()
            except Post.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def blocks(self, request, pk):
        user = self.get_object()
        serializer = TinyUserSerializer(
            user.blocked_user.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    @blocks.mapping.put
    def toggle_blocks(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if request.user != user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if pk is not None:
            try:
                blocking = User.objects.get(pk=pk)
                if blocking in user.blocked_user.all():
                    user.blocked_user.remove(blocking)
                else:
                    user.blocked_user.add(blocking)
                return Response()
            except User.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def follows(self, request, pk):
        user = self.get_object()
        serializer = TinyUserSerializer(
            user.following_user.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    @follows.mapping.put
    def toggle_follows(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if request.user != user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if pk is not None:
            try:
                following = User.objects.get(pk=pk)
                if following in user.following_user.all():
                    user.following_user.remove(following)
                else:
                    user.following_user.add(following)
                return Response()
            except User.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def game_list(self, request, pk):
        user = self.get_object()
        serializer = GameSerializer(
            user.game_list.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    @game_list.mapping.put
    def toggle_game_list(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if request.user != user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if pk is not None:
            try:
                game = Game.objects.get(pk=pk)
                if game in user.game_list.all():
                    user.game_list.remove(game)
                else:
                    user.game_list.add(game)
                return Response()
            except Game.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
