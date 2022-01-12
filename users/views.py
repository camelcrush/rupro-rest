from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from games.serializers import GameSerializer
from posts.models import Post
from posts.serializers import PostSerializer
import jwt
import os
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import UserSerializer, TinyUserSerializer
from .models import User
from games.models import Game
from games.serializers import GameSerializer
from .permissions import IsSelf
from .tokens import account_activation_token


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

    @action(detail=False, methods=["get"])
    def logout(self, request):
        logout(request)
        return Response()

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


class UserActive(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.active = True
                user.save()
                return Response(user.email + "계정이 활성화 되었습니다", status=status.HTTP_200_OK)
            else:
                return Response("만료된 링크입니다", status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response("계정활성화할 수 없습니다", status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def get(self, request):
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        response = redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
        return response


class KakaoCallback(APIView):
    def get(self, request):
        try:
            code = request.GET.get("code")
            client_id = os.environ.get("KAKAO_ID")
            redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
            token_request = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                return Response(
                    {"error_message": "인증코드를 받을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            email = profile_json.get("kakao_account").get("email", None)
            if email is None:
                return Response(
                    {"error_message": "이메일 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND
                )
            nickname = profile_json.get("properties").get("nickname", None)
            try:
                user = User.objects.get(email=email)
                if user.login_method != User.LOGIN_KAKAO:
                    return Response(
                        {"error_message": f"다음 경로로 로그인 하세요, {user.login_method}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except User.DoesNotExist:
                user = User.objects.create(
                    email=email,
                    username=email,
                    first_name=nickname,
                    login_method=User.LOGIN_KAKAO,
                    active=True,
                )
                user.set_unusable_password()
                user.save()
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        except Exception:
            return Response(
                {"error_message": "로그인할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
