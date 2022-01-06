from posts.models import Post
from posts.serializers import PostSerializer
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, TinyUserSerializer
from .models import User
from games.models import Game
from .permissions import IsSelf


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
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


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class LikesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PostSerializer(
            user.likes.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
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


class BlockView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = TinyUserSerializer(
            user.blocked_user.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
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


class FollowingView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = TinyUserSerializer(
            user.following_user.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
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


class GameListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = Game(user.game_list.all(), many=True, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
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
