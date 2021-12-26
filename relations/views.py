from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Relation
from .serializers import RelationSerializer


class RelationViewSet(ModelViewSet):

    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    serializer_class = RelationSerializer
    queryset = Relation.objects.all()
