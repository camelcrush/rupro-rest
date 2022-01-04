from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import GameScore
from .serializers import GameScoreSerializer
from .permissions import IsOwner


class GameScoreViewSet(ModelViewSet):

    queryset = GameScore.objects.all()
    serializer_class = GameScoreSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
