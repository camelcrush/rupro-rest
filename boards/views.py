from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from .models import Board
from .serializers import BoardsSerializer
from .permissions import IsOwner


class BoardViewSet(ModelViewSet):

    queryset = Board.objects.all()
    serializer_class = BoardsSerializer

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
        game = request.GET.get("game", None)
        filter_args = {}
        if game is not None:
            filter_args["game__contains"] = game
        try:
            boards = Board.objects.filter(**filter_args)
        except ValueError:
            boards = Board.objects.all()
        paginator = self.paginator
        results = paginator.paginate_queryset(boards, request)
        serializer = BoardsSerializer(results, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
