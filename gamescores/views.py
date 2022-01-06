from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import GameScore
from .serializers import GameScoreSerializer


class GameScoreViewSet(ModelViewSet):

    queryset = GameScore.objects.all()
    serializer_class = GameScoreSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create" or self.action == "partial_update":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
