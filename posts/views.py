from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions, status
from .models import Post
from .serializers import PhotoSerializer, PostSerializer
from .permissions import IsOwner


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        title = request.GET.get("title", None)
        game = request.GET.get("game", None)
        filter_args = {}
        if title is not None:
            filter_args["title__contains"] = title
        if game is not None:
            filter_args["game__contains"] = game
        try:
            posts = Post.objects.filter(**filter_args)
        except ValueError:
            posts = Post.objects.all()
        paginator = self.paginator
        results = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(results, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
