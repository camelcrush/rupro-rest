from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import UserGameScoreModel
from .serializers import UserGameScoreSerializer
from .permissions import IsOwner


class UserGameScoreViewSet(ModelViewSet):

    queryset = UserGameScoreModel.objects.all()
    serializer_class = UserGameScoreSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
